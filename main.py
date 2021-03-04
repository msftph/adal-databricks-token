from adal import AuthenticationContext
import requests

authority_host_url = "https://login.microsoftonline.com/"

# the Application ID of  AzureDatabricks
azure_databricks_resource_id = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"
databricks_instance = '<databricks-instance>'

# Required user input
user_parameters = {
   "tenant" : "<tenant-id>",
   "client_id" : "<application-id>",
   "username" : "<username>",
   "password" : "<password>"
}

def get_aad_token():
  # configure AuthenticationContext
  # authority URL and tenant ID are used
  authority_url = authority_host_url + user_parameters['tenant']
  context = AuthenticationContext(authority_url)

  # API call to get the token
  token_response = context.acquire_token_with_username_password(
    azure_databricks_resource_id,
    user_parameters['username'],
    user_parameters['password'],
    user_parameters['client_id']
  )

  return (token_response['accessToken'], token_response['refreshToken'])

def create_pat_with_aad_token(access_token):

  domain = databricks_instance
  token = access_token
  base_url = 'https://%s/api/2.0/token/create' % (domain)

  # request header
  headers = {
    'Authorization' : 'Bearer ' + token
  }

  response = requests.post(
    base_url,
    headers=headers,
    json = {
      "lifetime_seconds": 100,
      "comment": "this is an example token"
    }
  )

  print ('response header: ' + str(response.headers))
  print ('the response is: ' + str(response.content))
  
  try:
    print ('Decoding response as JSON... ')
    res_json = response.json()
    return res_json
        
  except Exception as e:
    print ('Response cannot be parsed as JSON:')
    print ('\t: ' + str(response))
    print ('The exception is: %s' % str(e))

def print_pat(pat):
  print ('token_value: ' + str(pat["token_value"]))
  print ('token_info.token_id: ' + str(pat["token_info"]["token_id"]))
  print ('token_info.creation_time: ' + str(pat["token_info"]["creation_time"]))
  print ('token_info.expiry_time: ' + str(pat["token_info"]["expiry_time"]))
  print ('token_info.comment: ' + str(pat["token_info"]["comment"]))

(access_token, refresh_token) = get_aad_token()
pat = create_pat_with_aad_token(access_token)
print_pat(pat)