from s3_textract_functions import *
import boto3

def datachunk(x):
    """Comprehend accepts textfile upto 5000 bytes only. More than that we need to chunk it into a list of textfiles"""
    y=[]
    while x:
        y.append(str(x[:5000]))
        x=x[5000:]
    return y
    
def lambda_handler(event, context):
    
    bucketName=''
    fileName=''
    jobId = startJob(bucketName, fileName)
    print(f"Started job with id: {jobId}")
    response=getJobResults(jobId)
    
    # Writing Textract Output to Text:
    textFile=''
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            textFile+=item["Text"]+' '
            
    comp=boto3.client('comprehend')
    entitty=comp.batch_detect_entities(TextList=datachunk(textFile), LanguageCode='en')
    
    for i in entitty['ResultList']:
        for j in i['Entities']:
            if j['Type']=='ORGANIZATION':
                print(j['Text'])
   
    return "done"
