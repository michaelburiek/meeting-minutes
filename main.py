import re
import os
import asyncio
import configparser
from graph_api import Graph
from openai_api import OpenAIHelper
from utils import Utils
from msgraph.generated.models.o_data_errors.o_data_error import ODataError


async def main():
    print('Meeting Minutes App\n')

    # LOAD APP SETTINGS
    # config = configparser.ConfigParser()
    # config.read(['config.cfg'])
    # azure_settings = config['azure']
    # graph: Graph = Graph(azure_settings)

    # MEETING MINUTES APP
    try:
        print('Meeting Minutes App')

        # Request the event ID from the user
        # event_id = input("Please enter the event ID: ")

        # Call the get_meeting_transcript function with the user-provided event ID
        # transcript = await graph.get_meeting_transcript(event_id)

        # CURRENT WORK AROUND JUST UPLOADING THE MEETING TRANSCRIPT
        utils = Utils()

        # Request files from user
        print("Meeting transcript: ")
        meeting_transcript = await utils.ask_for_file()
        print("Context: ")
        context = await utils.ask_for_file()

        # Print the path to the file chosen by the user
        if meeting_transcript:
            print(f"Meeting transcript: {meeting_transcript}")

        # Clean up meeting transcript
        await utils.clean_up_transcript(meeting_transcript)

        # Create one line of text from meeting transcript
        transcript = await utils.file_to_oneliner(meeting_transcript)
        context = await utils.file_to_oneliner(context)

        print("Context: " + context)
        print("Transcript: " + transcript)

        # Load the API key from the environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found in environment variable")

        # Initialize the OpenAI helper class
        openai_helper = OpenAIHelper(api_key)

        # Format messages to send to OpenAI
        prompt = openai_helper.create_prompt(context, transcript)

        # Get chat response
        chat_response = await openai_helper.chat_with_openai(prompt)
        print("Meeting minutes:", chat_response)

    except ODataError as odata_error:
        print('Error:')
        if odata_error.error:
            print(odata_error.error.code, odata_error.error.message)

# RUN MAIN
asyncio.run(main())
