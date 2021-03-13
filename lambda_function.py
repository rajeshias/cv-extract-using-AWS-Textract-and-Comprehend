from s3_textract_functions import *
import codecs
import json, boto3
from pprint import pprint


def lambda_handler(event, context):
    bucketName = 'cvreader'
    fileName = 'vijaymamacv.pdf'
    jobId = startJob(bucketName, fileName)
    print(f"Started job with id: {jobId}")
    response = getJobResults(jobId)

    # Writing Textract Output to Text:
    textFile = ''
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            textFile += item["Text"] + ' '

    comp = boto3.client('comprehend')

    entitty = comp.detect_entities(Text=textFile, LanguageCode='en')

    # batchkp=comp.batch_detect_key_phrases(TextList=datachunker(para),LanguageCode='en') //batch_detect_entities, batch_detect_sentiment, etc
    # keyp=comp.detect_key_phrases(Text=textFile, LanguageCode='en')
    # res=comp.detect_sentiment(Text=para, LanguageCode='en')

    # s3=boto3.client("s3").get_object(Bucket="redditwritingpromptssample", Key="Textcomprehend.txt")
    # para=str(s3['Body'].read())
    # comp=boto3.client('comprehend')
    # res=comp.detect_sentiment(Text=para, LanguageCode='en')
    # entitty=comp.detect_entities(Text=para, LanguageCode='en')
    # batchkp=comp.batch_detect_key_phrases(TextList=datachunker(para),LanguageCode='en') //batch_detect_entities, batch_detect_sentiment, etc
    # keyp=comp.detect_key_phrases(Text=para, LanguageCode='en')

    for i in entitty['Entities']:
        if i['Type'] == 'TITLE':
            print(i['Text'])

    # pprint(keyp)
    # print(res)
    # pprint(batchkp)

    return "done"