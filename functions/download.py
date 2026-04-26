import requests
import base64

def handler(event, context):
    # User එවන Link එක මෙතනින් ගන්නවා
    query_params = event.get('queryStringParameters', {})
    target_url = query_params.get('url')
    
    # ලින්ක් එකක් නැතිනම් Error එකක් යවනවා
    if not target_url:
        return {
            "statusCode": 400, 
            "body": "Error: Please provide a valid URL."
        }

    try:
        # File එක Download කරගන්නවා (15s timeout එකක් එක්ක)
        response = requests.get(target_url, timeout=15)
        response.raise_for_status()

        # Netlify හරහා binary data යවන්න නම් Base64 කරන්න ඕනේ
        file_content = base64.b64encode(response.content).decode("utf-8")
        
        # URL එකෙන් File එකේ නම හොයාගන්නවා
        filename = target_url.split("/")[-1]
        if not filename or "?" in filename:
            filename = "downloaded_file"

        return {
            "statusCode": 200,
            "headers": {
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": response.headers.get('Content-Type', 'application/octet-stream'),
                "Access-Control-Allow-Origin": "*"
            },
            "body": file_content,
            "isBase64Encoded": True
        }

    except requests.exceptions.RequestException as e:
        return {
            "statusCode": 500,
            "body": f"Network Error: {str(e)}"
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"System Error: {str(e)}"
        }
