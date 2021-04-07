
class ProjectManager:

    temp_file = "files/temp.py"
    template_general = "core/templates/general.pyt"
    template_instrument = "core/templates/instrument.pyt"

    def __init__(self):
        self.instruments = {}
    
    def save(self,info,path):
        file = open(path,"w")
        
        write = ";;;".join([
            info["MAX_VOL"],
            info["OUTFILE"],
            info["SAMPLERATE"],
            info["MAX_LEN"],
            info["NOTES"],
            info["INS_NAME"] # active instrument
        ])
        for name,ins in self.instruments.items():
            write += ";;;"+name+";;"+ins

        file.write(write)
        file.close()
    
    def load(self,path):
        file = open(path,"r")
        
        info = {}
        ctc = file.read().split(";;;")

        file.close()

        info["MAX_VOL"] = ctc.pop(0)
        info["OUTFILE"] = ctc.pop(0)
        info["SAMPLERATE"] = ctc.pop(0)
        info["MAX_LEN"] = ctc.pop(0)
        info["NOTES"] = ctc.pop(0)
        info["INS_NAME"] = ctc.pop(0)

        self.instruments = { t.split(";;")[0]:t.split(";;")[1] for t in ctc} 
        
        info["INS_CODE"] = self.instruments[info["INS_NAME"]]

        return info


    def ins_new(self):
        name = "Instrument "+str(len(self.instruments.keys()))
        self.instruments[name] = ""
        return name

    def ins_del(self,name):
        del self.instruments[name]

    def ins_update(self,name,code):
        if name == "":return
        self.instruments[name] = code

    def compile(self,compileInfo):
        try:
            
            f_ins = open(self.template_instrument,"r")
            c_ins = f_ins.read()
            f_ins.close()

            instrument_out = ""
            for name,instrument in self.instruments.items():
                instrument_out += c_ins.replace("{#INS_NAME#}",name).replace("{#INS_CODE#}",instrument.code.replace("\n","\n  "))

            f_general = open(self.template_general,"r")
            c_general = f_general.read()
            f_general.close()

            general_replace = {
                "{#MAX_VOL#}":str(compileInfo["MAX_VOL"]),
                "{#SAMPLERATE#}":str(compileInfo["SAMPLERATE"]),
                "{#MAX_LEN#}":str(compileInfo["MAX_LEN"]),
                "{#INS_TEMPLATE#}":self.notes,
                "{#OUT_FILE#}":self.temp_file,
                "{#NOTES#}":self.notes
            }

            for k,v in general_replace.items():c_general.replace(k,v)

            f_out = open(self.template_instrument,"w")
            f_out.write(c_general)
            f_out.close()

        except FileNotFoundError:
            print("Template file missing.")
