class Config :
    JWT_SECRET_KEY = 'yh@1234'
    
    ACCESS_KEY = "AKIAW5QZZAQHEJCUXX5E"
    SECRET_ACCESS = "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"
    
    S3_BUCKET = "hanul0147-image-test"
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)