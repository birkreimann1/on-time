# onTime - Transit Delay Tracker
onTime is an app which allows users to selectively look at bus stations in Lübeck and get a score on the upcoming departures based on the historical delays of the bus lines.
Website: https://ontime-e0281.web.app/
## Hackathon setup
The following section explains in detail how to setup a machine to develop the app
### Downloads
1. Install VS Code: https://code.visualstudio.com/
2. Install node.js: https://nodejs.org/en
3. Install Fork: https://git-fork.com/
4. Install FirebaseCLI
    ```markdown
	npm install -g firebase-tools
    ```
### Setup project
1. Login to Fork with your git credentials
2. Clone the repository: https://github.com/birkreimann1/on-time.git
3. Install dependencies inside your repository folder:
    ```markdown
	npm install firebase
    npm install -g live-server
    ```
4. The project should already be initialised. To run the project on a live server run the following command:
    ```markdown
	live-server
    ``` 
5. To deploy the local changes to firebase run:
    ```markdown
	firebase login
    firebase init hosting           # optional, should work already
    firebase deploy
    ``` 
