from fastapi import FastAPI, Request


app = FastAPI()


@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    action = payload.get("action")

    repository = payload.get("repository", {})
    owner = repository.get("owner", {}).get("login")
    repository_name = repository.get("name")

    pull_request = payload.get("pull_request", {})
    pull_number = pull_request.get("number")

    installation = payload.get("installation", {})
    installation_id = installation.get("id")

    print("GitHub webhook received")
    print("Action:", action)
    print("Owner:", owner)
    print("Repository:", repository_name)
    print("Pull request:", pull_number)
    print("Installation ID:", installation_id)

    return {
        "status": "received",
    }