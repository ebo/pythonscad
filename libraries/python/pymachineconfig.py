import os
import json


"""
MachineConfig class which can be used to read lasercutter and 3D
printer machine and material configurations.  The config file is
cached as a JSON export of python dictionaries.
"""
class MachineConfig:

    _config = {}
    _default = {}

    # FIXME: ~/.config/PythonSCAD/
    def __init__(self, name="PythonSCAD.json"):
        try:
            self._config = self.read_config(name)
            self._default = self.working_config(label="default")
        except:
            pass
        return

    def gen_tst_config(self, name="PythonSCAD.json"):
        # FIXME: this is just an expeerimental hack to get started.

        # FIXME:
        cfg = [
            # what is the default configuration?
            {"label":"default",
             "type":"default",
             "property":{"machine":"Creality-Falcon2",
                         "head":"LED-40",
                         "material":"3mm_ply_LED-40"
                         }
             },
            # different machine configurations
            {"label":"Creality-Falcon2",
             "type":"machine",
             "property":{"max_feed":25000, #(mm/min)
                         "max_width":400, #(mm)
                         "max_len":415, #(mm)
                         "has_camera":False
                         }
             },
            {"label":"XTool-S1",
             "type":"machine",
             "property":{"max_feed":36000, #(mm/min)
                         "max_width":319, #(mm)
                         "max_len":498, #(mm)
                         "has_camera":False
                         }
             },
            # different heads which can be independent of a given
            # machine
            {"label":"LED-40",
             "type":"head",
             "property":{"max_power":40.0, # (W)
                         "wavelength":455, #(nm)
                         "has_air":True,
                         "kerf": 0.075
                         },
             },
            {"label":"LED-20",
             "type":"head",
             "property":{"max_power":240.0, # (W)
                         "wavelength":455, #(nm)
                         "has_air":True,
                         "kerf": 0.075
                         },
             },
            # materials which are dependent on the head
            # characteristics. The machines assume units in mm and
            # minutes.
            {"label":"3mm_ply_LED-40",
             "type":"material",
             "property":{"thickness":3.0, # (mm)
                         "cut_power":40.0, # (W)
                         "cut_feed":400, # (mm/min)
                         "engrave_power":30.0, # (W)
                         "engrave_feed":6000 # (mm/min)
                         },
             },

            {"label":"0.25in_ply_LED-40",
             "type":"material",
             "property":{"thickness":6.35,
                         "cut_power":40.0,
                         "cut_feed":200,
                         "engrave_power":30.0,
                         "engrave_feed":6000
                         },
             },
            {"label":"0.75in_pine_LED-40",
             "type":"material",
             "property":{"thickness":19.05,
                         "cut_power":40.0,
                         "cut_feed":15,
                         "engrave_power":30.0,
                         "engrave_feed":6000
                         },
             },
        ]

        return cfg

    def read_config(self, name="PythonSCAD.json"):
        if '~' in name:
            name = name.replace('~',os.path.expanduser("~"))
        with open(name, 'r', encoding='utf-8') as f:
            cfg = json.loads(f.read())
            return cfg
        
    def write_config(self, name="PythonSCAD.json", config=None):
        if '~' in name:
            name = name.replace('~',os.path.expanduser("~"))

        if config is None:
            config = self._config

        jstr = json.dumps(config, indent=4)

        if jstr is not None:
            with open(name,'w') as fout:
                fout.write(jstr)
        
        return

    def set_config(self, config):
        self._config = config
        return

    def dict(self):
        return self._config

    def get_machine(self, machine=None):
        default = self._config["default"]
        machine = default["machine"]
        head = default["head"]
        print("***",default)
        

    def set_default(self, default):
        #...
        return

    def get_types(self):
        types = set([x["type"] for x in self._config])
        return types
    
    def get_label_by_type(self, label):
        values = set([x["label"] for x in self._config if x["type"]==label])
        return values
    
    def get_value_by_label(self, label1, label2):
        dicts = [x for x in self._config if x["label"]==label1]
        values = [x[label2] for x in dicts]
        return values

    def get_sublabel(self, label, value):
        dicts = [x for x in self._config if x["type"]==label]
        values = [x[value] for x in dicts]
        return values

    def working_config(self, label="default"):
        if self._default:
            return self._default

        ncfg = {}
        
        dcfg = self.get_sublabel(label,"property")[0]

        lbls = dcfg.keys()

        for l in lbls:
            k = dcfg[l]
            tcfg = self.get_value_by_label(k,"property")
            for i in range(len(tcfg)):
                for tk in tcfg[i].keys():
                    ncfg[tk] = tcfg[i][tk]

        self._default = ncfg
        
        return self._default

