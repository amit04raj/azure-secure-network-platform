from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Azure Secure Network Platform",
    description="A cloud security and networking demonstration platform.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

STORAGE_ACCOUNT_URL = "https://stsecnetworkplatform01.blob.core.windows.net/"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "azure-secure-network-platform",
    }


@app.get("/storage-test")
async def storage_test():
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(
        account_url=STORAGE_ACCOUNT_URL,
        credential=credential,
    )

    containers = list(blob_service_client.list_containers())

    return {
        "status": "connected",
        "storage_account": "stsecnetworkplatform01",
        "container_count": len(containers),
    }