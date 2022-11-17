import logging

#logging.basicConfig(filename='utils/pipePackage/example.log', encoding='utf-8', level=logging.DEBUG)
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')
#logging.error('And non-ASCII stuff, too, like Øresund and Malmö')

logger = logging.getLogger(__name__)  
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='/opt/pipeline/log/pipeline.log', mode='w+')
formatter = logging.Formatter('%(asctime)s : %(name)s  : %(funcName)s : %(levelname)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

for i in range(20):
    logger.info("Fatto un log")