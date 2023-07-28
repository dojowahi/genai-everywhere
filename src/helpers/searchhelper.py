import pandas as pd
import json
from google.cloud import discoveryengine_v1beta as genappbuilder
import pandas as pd
import json
from typing import Union
from google.protobuf.json_format import MessageToDict
from google.cloud import aiplatform
from vertexai.language_models._language_models import TextGenerationModel, ChatModel
import os
from dotenv import load_dotenv
import logging
from os.path import basename
from typing import List, Optional, Tuple
from langchain.chains import (
    RetrievalQA,
    RetrievalQAWithSourcesChain,
    ConversationalRetrievalChain,
)
from langchain.memory import ConversationBufferMemory
import vertexai
from langchain.llms import VertexAI

# from langchain.retrievers import GoogleCloudEnterpriseSearchRetriever
from helpers.vidhelper import initialize_llm
from google.cloud import discoveryengine, discoveryengine_v1beta

load_dotenv()

# Custom functions
bucket_name = os.getenv("bucket_name")
project_id = os.getenv("project_id")
location = os.getenv("region")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_with_summary(
    project_id: str,
    location: str,
    data_store: str,
    temperature: float,
    search_query: str,
) -> str:
    # Gen App Builder Enterprise Search
    try:
        client = genappbuilder.SearchServiceClient()
        # The full resource name of the search engine serving config
        # e.g. projects/{project_id}/locations/{location}
        serving_config = client.serving_config_path(
            project=project_id,
            location="global",
            data_store=data_store,
            serving_config="default_config",
        )

        request = genappbuilder.SearchRequest(
            serving_config=serving_config,
            query=search_query,
        )
        response = client.search(request)
        logger.info(f"Search query {search_query} and Search response: {str(response)}")
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
    results = []
    for res in response.results:
        results.append(res)

    # to results dataframe
    response = MessageToDict(results[0]._pb)
    results_dataframe = pd.DataFrame.from_dict(get_documents(results))

    # construct references
    # print("JSON data created from the search results!")
    references_dataframe = getSnippets(results_dataframe)
    logger.info(f"Dataframe: {references_dataframe.to_json(orient='records')}")

    # Summarize with PaLM
    aiplatform.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained("text-bison@001")

    prompt = f"""
The following are the results from a query "{search_query}" in JSON format.
Using only the JSON below, summarize the JSON to provide an answer.
Make sure not to use any citations for the summary except for what's contained in the JSON below.
Once you've created a summary, append to the summary a list of citations relevant in creating 
the summary from link and title values in the JSON, with each citation in the form of 
"found in 'title' article, at 'link'"

{references_dataframe.to_json(orient='records')}
"""

    prediction = model.predict(
        prompt,
        # Optional:
        max_output_tokens=1024,
        temperature=temperature,
        top_p=0.8,
        top_k=40,
    )

    safety_categories = prediction._prediction_response[0][0]["safetyAttributes"]
    if safety_categories["blocked"]:
        msg = "This response was blocked due to safety concerns. Please restate your question."
        logger.info(msg)
        logger.info(
            f"""The prompt that was blocked is as follows:
        {prompt}
        """
        )
    else:
        msg = prediction
        logger.info(f"Prediction:->{prediction}")
        logger.info(f"Prediction Type:->{type(prediction)}")
        logger.info(f"Prediction Modules:->{dir(prediction)}")
    return msg, references_dataframe


def search(
    project_id: str,
    location: str,
    data_store: str,
    temperature: float,
    search_query: str,
) -> Union[list, pd.DataFrame]:
    client = genappbuilder.SearchServiceClient()

    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = client.serving_config_path(
        project=project_id,
        location="global",
        data_store=data_store,
        serving_config="default_config",
    )

    request = genappbuilder.SearchRequest(
        serving_config=serving_config,
        query=search_query,
    )
    response = client.search(request)
    results = []
    for res in response.results:
        results.append(res)
    return results, pd.DataFrame(results)


def get_documents(objects):
    """
    Return a list of documents from a list of objects.
    """
    docs = []
    for doc in objects:
        response = MessageToDict(doc._pb)
        docs.append(response["document"])
    return docs


def getSnippets(df):
    newdf = pd.DataFrame()
    data = df.loc[:, "derivedStructData"]

    for idx, item in data.items():
        # item is a dict now
        for removeKey in [
            "htmlFormattedUrl",
            "pagemap",
            "htmlTitle",
            "displayLink",
            "formattedUrl",
        ]:
            if removeKey in item:
                del item[removeKey]
        # print(sorted(item.keys()))
        d = pd.Series(item, name=idx)
        item["snippet"] = d["snippets"][0]["snippet"]
        newdf = pd.concat([newdf, pd.DataFrame.from_dict(item)], ignore_index=True)

    newdf = newdf.drop(columns=["snippets"])
    return newdf


JSON_INDENT = 2


def list_documents(
    project_id: str,
    location: str,
    datastore_id: str,
) -> List[discoveryengine.Document]:
    client = discoveryengine.DocumentServiceClient()

    parent = client.branch_path(
        project=project_id,
        location=location,
        data_store=datastore_id,
        branch="default_branch",
    )

    request = discoveryengine.ListDocumentsRequest(parent=parent, page_size=10)

    page_result = client.list_documents(request=request)

    return [
        {"id": document.id, "title": basename(document.content.uri)}
        for document in page_result
    ]


def search_enterprise_search(
    project_id: str,
    location: str,
    search_engine_id: str,
    search_query: str,
) -> Tuple:
    # Create a client
    client = discoveryengine.SearchServiceClient()

    # The full resource name of the search engine serving config
    # e.g. projects/{project_id}/locations/{location}
    serving_config = client.serving_config_path(
        project=project_id,
        location="global",
        data_store=search_engine_id,
        serving_config="default_config",
    )

    request = discoveryengine.SearchRequest(
        serving_config=serving_config,
        query=search_query,
        page_size=50,
        content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
            snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                max_snippet_count=1
            )
        ),
    )
    response_pager = client.search(request)

    response = discoveryengine.SearchResponse(
        results=response_pager.results,
        facets=response_pager.facets,
        guided_search_result=response_pager.guided_search_result,
        total_size=response_pager.total_size,
        attribution_token=response_pager.attribution_token,
        next_page_token=response_pager.next_page_token,
        corrected_query=response_pager.corrected_query,
        summary=response_pager.summary,
    )

    request_url = f"https://discoveryengine.googleapis.com/v1/{serving_config}:search"

    request_json = discoveryengine.SearchRequest.to_json(
        request, including_default_value_fields=True, indent=JSON_INDENT
    )
    response_json = discoveryengine.SearchResponse.to_json(
        response,
        including_default_value_fields=True,
        indent=JSON_INDENT,
    )

    results = get_enterprise_search_results(response)
    logger.info(f"Results:->{results}")
    logger.info(f"Results Type:->{type(results)}")
    logger.info(f"Results Modules:->{dir(results)}")
    return results, request_url, request_json, response_json


def get_enterprise_search_results(response: discoveryengine.SearchResponse) -> List:
    """
    Extract Results from Enterprise Search Response
    """

    results = []
    for result in response.results:
        data = result.document.derived_struct_data

        cse_thumbnail = data["pagemap"].get("cse_thumbnail")
        if cse_thumbnail:
            image = cse_thumbnail[0]["src"]
        else:
            image = "https://www.google.com/images/errors/robot.png"
        results.append(
            {
                "title": data["title"],
                "htmlTitle": data["htmlTitle"],
                "link": data["link"],
                "htmlFormattedUrl": data["htmlFormattedUrl"],
                "displayLink": data["displayLink"],
                "snippets": [s["htmlSnippet"] for s in data["snippets"]],
                "thumbnailImage": image,
                "resultJson": discoveryengine.SearchResponse.SearchResult.to_json(
                    result,
                    including_default_value_fields=True,
                    indent=JSON_INDENT,
                ),
            }
        )

    return results


# def retrieval_qa_es(search_query, search_engine_id):
#     llm, embedding, retriever = initialize_llm(search_engine_id=search_engine_id)
#     logger.info(f"Query:{search_query}, Engine:{search_engine_id}")
#     retrieval_qa_with_sources = RetrievalQAWithSourcesChain.from_chain_type(
#         llm=llm, chain_type="stuff", retriever=retriever
#     )

#     results = retrieval_qa_with_sources(
#         {"question": search_query}, return_only_outputs=True
#     )
#     return results
