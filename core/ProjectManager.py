import os
import winsound


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
        name = "ins_"+str(len(self.instruments.keys()))
        self.instruments[name] = ""
        return name

    def ins_del(self,name):
        del self.instruments[name]

    def ins_update(self,name,code):
        if name == "":return
        self.instruments[name] = code

    def stop_sound(self):
        winsound.PlaySound(None, winsound.SND_PURGE)

    def compile(self,compileInfo):
        try:
            
            f_ins = open(self.template_instrument,"r")
            c_ins = f_ins.read()
            f_ins.close()

            instrument_out = ""
            for name,code in self.instruments.items():
                instrument_out += c_ins.replace("{#INS_NAME#}",name).replace("{#INS_CODE#}","  "+code.replace("\n","\n  "))

            f_general = open(self.template_general,"r")
            c_general = f_general.read()
            f_general.close()

            print("Instrument out is",instrument_out)

            general_replace = {
                "{#MAX_VOL#}":compileInfo["MAX_VOL"],
                "{#SAMPLERATE#}":compileInfo["SAMPLERATE"],
                "{#MAX_LEN#}":compileInfo["MAX_LEN"],
                "{#INS_TEMPLATE#}":instrument_out,
                "{#OUT_FILE#}":compileInfo["OUTFILE"],
                "{#NOTES#}":compileInfo["NOTES"]
            }

            for k,v in general_replace.items():
                print("replacing",k,"for",v)
                c_general = c_general.replace(k,v)


            f_out = open(self.temp_file,"w")
            f_out.write(c_general)
            f_out.close()

            print("Compilation done, running sys")
            os.system("python \""+self.temp_file+'"')

            winsound.PlaySound(compileInfo["OUTFILE"], winsound.SND_ASYNC)

        except FileNotFoundError:
            print("Template file missing.")
