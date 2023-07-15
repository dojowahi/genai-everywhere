# Gen AI Everywhere All at Once
The goal of this demo is to deploy Gen AI apps on Cloud run

## Requirements
* Ensure the GCP user is allowed to create service accounts and assign roles


## Setting up the demo
**1)** In Cloud Shell or other environment where you have the gcloud SDK installed, execute the following commands:
```console
gcloud components update 
cd $HOME
git clone https://github.com/dojowahi/genai-everywhere.git
cd ~/genai-everywhere
chmod +x *.sh
```

**2)** **Edit config.sh** - In your editor of choice update the variables in config.sh to reflect your desired gcp project.

**3)** Next execute the command below

```console
sh setup_argolis.sh
```
If the shell script has executed successfully, you should now have a new GCP project created, based on the name in your config.sh
<br/><br/>

**4)** Next execute the command below

```console
sh setup_sa.sh
```
If the shell script has executed successfully, you should now have a new Service Account created.
<br/><br/>


**5)** Next execute the command below

```console
sh -x deploy.sh
```

If the shell script has executed successfully,you will have a Cloud run URL displayed on the console.
locking on the URL should take you to the app 


### Congrats! You just deployed a Gen AI app on Cloud Run
