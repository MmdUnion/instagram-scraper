import uvicorn

config = {}

config['log_config'] = {
   "version":1,
   "disable_existing_loggers":True,
   "formatters":{
      "default":{
         "()":"uvicorn.logging.DefaultFormatter",
         "fmt":"%(levelprefix)s %(message)s",
         "use_colors":"None"
      },
      "access":{
         "()":"uvicorn.logging.AccessFormatter",
         "fmt":"%(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
      }
   },
   "handlers":{
      "default":{
         "formatter":"default",
         "class":"logging.StreamHandler",
         "stream":"ext://sys.stderr"
      },
      "access":{
         "formatter":"access",
         "class":"logging.StreamHandler",
         "stream":"ext://sys.stdout"
      }
   },
   "loggers":{
      "uvicorn":{
         "handlers":[
            "default"
         ],
         "level":"INFO"
      },
      "uvicorn.error":{
         "level":"INFO",
         "handlers":[
            "default"
         ],
         "propagate":True
      },
      "uvicorn.access":{
         "handlers":[
            "access"
         ],
         "level":"INFO",
         "propagate":False
      }
   }
}

config['log_config']['loggers']['quart'] = {
   "handlers":[
      "default"
   ],
   "level":"INFO"
}

if __name__ == '__main__':
    uvicorn.run("main:app", **config)
