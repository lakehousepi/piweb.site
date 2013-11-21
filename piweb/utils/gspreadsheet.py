import gdata.spreadsheet.service as gdss

class GSpreadsheetUpdater(object):
    def __init__(self, username, password, source, spreadsheetkey, worksheetid):
        self.username = username
        self.password = password
        self.source = source
        self.spreadsheetkey = spreadsheetkey
        self.worksheetid = worksheetid
        
    def login(self):
        self.spr_client = gdss.SpreadsheetsService()
        self.spr_client.email = self.username
        self.spr_client.password = self.password
        self.spr_client.source = 'RaspberryPi data insertion script'
        self.spr_client.ProgrammaticLogin()
    
    def insertrow(self, datadict):
        self.login()
        result = self.spr_client.InsertRow(
            datadict, 
            self.spreadsheetkey,
            self.worksheetid
        )
        return result