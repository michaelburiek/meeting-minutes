from typing import Dict, Any
from configparser import SectionProxy
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.users.users_request_builder import UsersRequestBuilder


class Graph:
    settings: SectionProxy
    client_credential: ClientSecretCredential
    app_client: GraphServiceClient

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['clientSecret']

        self.client_credential = ClientSecretCredential(
            tenant_id, client_id, client_secret)
        self.app_client = GraphServiceClient(
            self.client_credential)

    # <GetAppOnlyTokenSnippet>
    async def get_app_only_token(self):
        graph_scope = 'https://graph.microsoft.com/.default'
        access_token = await self.client_credential.get_token(graph_scope)
        return access_token.token
    # </GetAppOnlyTokenSnippet>

    # <GetMeetingTranscriptSnippet>
    async def get_meeting_transcript(self, event_id: str) -> Dict[str, Any]:
        # Define the endpoint to get event attachments
        endpoint = f"/me/events/{event_id}/attachments"

        # Get the access token using the previously defined method
        access_token = await self.get_app_only_token()
        headers = {'Authorization': f'Bearer {access_token}'}

        # Make the API call to get event attachments
        attachments = await self.app_client.get(endpoint, headers=headers)

        # Assuming the transcript is an attachment, filter out the one you need
        for attachment in attachments['value']:
            if 'transcript' in attachment['name'].lower():
                # If it's a file attachment with a contentUrl, that's your transcript file
                if 'contentUrl' in attachment:
                    transcript_url = attachment['contentUrl']
                    # You might need to make another API call to get the file content
                    transcript_content = await self.app_client.get(transcript_url, headers=headers)
                    return transcript_content.json()

        # If no transcript is found
        return {"message": "No transcript found for the event"}
    # </GetMeetingTranscriptSnippet>
