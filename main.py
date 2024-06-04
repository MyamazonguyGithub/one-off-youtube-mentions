from algorithms.match import count_mentions
from datetime import datetime
from dotenv import load_dotenv
from os import getenv
from services.fireflies import fireflies_get_transcript
from services.gspread import gspread_try_clear_with_ranges, gspread_try_get_all_records, gspread_try_get_service_account_from_dict, gspread_try_get_spreadsheet_by_id, gspread_try_get_worksheet_by_id, gspread_try_update_acell, gspread_try_update_range
from time import sleep

load_dotenv()

if __name__ == '__main__':
    service_account_b = gspread_try_get_service_account_from_dict({
        "type": "service_account",
        "project_id": "integrations-set-6",
        "private_key_id": getenv("GSERVICE_B_PRIVATE_KEY_ID", ""),
        "private_key": getenv("GSERVICE_B_PRIVATE_KEY", ""),
        "client_email": "development@integrations-set-6.iam.gserviceaccount.com",
        "client_id": getenv("GSERVICE_B_CLIENT_ID", ""),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/development%40integrations-set-6.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    })

    spreadsheet = gspread_try_get_spreadsheet_by_id(service_account_b, '1v2T9DJGZ1t-XfBBR2xuDW3ll3WrNOTT7jadT0qolbhA')
    sheet = gspread_try_get_worksheet_by_id(spreadsheet, 0)
    transcript_records = gspread_try_get_all_records(sheet, head = 2)

    # Will keep this here for testing purposes
    test_transcript = """
        During our recent call with a prospective client, they mentioned that they had previously worked with cellar interactive. They appreciated the detailed reports provided but felt the customer service could be improved.

        Later in the conversation, the client brought up another competitor, canopy, and praised their innovative marketing strategies. However, they were not satisfied with the pricing plans offered by canapoy.

        Towards the end of the call, another competitor was mentioned, tenuity. The client highlighted that they found tinutty’s approach to be very aggressive but effective in driving sales. teaka

        Finally, the client discussed their experience with teka, noting that teaka had a very user-friendly platform but faced some issues with data synchronization. 

        seller interactive
        seller interactive
        tinuiti
        tenuity
        tinutty
    """


    # Calculate the start index for the last half of the list
    start_index = len(transcript_records) // 2
    
    for transcript_record in reversed(transcript_records[start_index:]):
        # Process transcript
        transcript = fireflies_get_transcript(transcript_record['ID'])
        count = count_mentions(transcript)
        remarks = '' if transcript else 'Has issues'
    
        # Convert unix timestamp to pretty datetime
        timestamp = int(transcript_record['Timestamp'])
        datetime_object = datetime.fromtimestamp(timestamp / 1000.0)
        pretty_datetime = datetime_object.strftime('%B %d, %Y, %I:%M%p')
    
        # Update the sheet
        row = [[pretty_datetime, count['Seller Interactive'], count['Canopy'], count['Tinuiti'], count['Teika'], remarks]]
        gspread_try_update_range(sheet, f'J{transcript_record["Row"]}', row)
        sleep(0.5)
        