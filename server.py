import uvicorn

if __name__ == '__main__':
    uvicorn.run("app.main:app",
                host="0.0.0.0",
                port=8432,
                reload=True,
                ssl_keyfile=r"C:\Users\isaact\Documents\attain2.key.pem", 
                ssl_certfile=r"C:\Users\isaact\Documents\attain.cert.pem"
                # ssl_keyfile=r"C:\Users\isaact\localhost+4-key.pem", 
                # ssl_certfile=r"C:\Users\isaact\localhost+4.pem"
                )