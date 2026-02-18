import os
import json


"""
MachineConfig class which can be used to read lasercutter and 3D
printer machine and material configurations.  The config file is
cached as a JSON export of python dictionaries.
"""
class MachineConfig:

    _config = {}  # the config as read in from the config file
    _working = {} # the, possibly modified, collapsed working config

    def __init__(self, name="PythonSCAD.json"):
        try:
            self._config = self.read(name)
        except:
            pass
        self._working = self.working_config(label="default")
        return

    def gen_color_table(self):
        color_table = {
            "label":"ColorTable",
            "type":"ColorTable",
            "property":{
                "L00": {"power":1.0,"feed":1.0,"color":0x000000},
                "L01": {"power":1.0,"feed":1.0,"color":0x0000FF},
                "L02": {"power":1.0,"feed":1.0,"color":0xFF0000},
                "L03": {"power":1.0,"feed":1.0,"color":0x00E000},
                "L04": {"power":1.0,"feed":1.0,"color":0xD0D000},
                "L05": {"power":1.0,"feed":1.0,"color":0xFF8000},
                "L06": {"power":1.0,"feed":1.0,"color":0x00E0E0},
                "L07": {"power":1.0,"feed":1.0,"color":0xFF00FF},
                "L08": {"power":1.0,"feed":1.0,"color":0xB4B4B4},
                "L09": {"power":1.0,"feed":1.0,"color":0x0000A0},
                "L10": {"power":1.0,"feed":1.0,"color":0xA00000},
                "L11": {"power":1.0,"feed":1.0,"color":0x00A000},
                "L12": {"power":1.0,"feed":1.0,"color":0xA0A000},
                "L13": {"power":1.0,"feed":1.0,"color":0xC08000},
                "L14": {"power":1.0,"feed":1.0,"color":0x00A0FF},
                "L15": {"power":1.0,"feed":1.0,"color":0xA000A0},
                "L16": {"power":1.0,"feed":1.0,"color":0x808080},
                "L17": {"power":1.0,"feed":1.0,"color":0x7D87B9},
                "L18": {"power":1.0,"feed":1.0,"color":0xBB7784},
                "L19": {"power":1.0,"feed":1.0,"color":0x4A6FE3},
                "L20": {"power":1.0,"feed":1.0,"color":0xD33F6A},
                "L21": {"power":1.0,"feed":1.0,"color":0x8CD78C},
                "L22": {"power":1.0,"feed":1.0,"color":0xF0B98D},
                "L23": {"power":1.0,"feed":1.0,"color":0xF6C4E1},
                "L24": {"power":1.0,"feed":1.0,"color":0xFA9ED4},
                "L25": {"power":1.0,"feed":1.0,"color":0x500A78},
                "L26": {"power":1.0,"feed":1.0,"color":0xB45A00},
                "L27": {"power":1.0,"feed":1.0,"color":0x004754},
                "L28": {"power":1.0,"feed":1.0,"color":0x86FA88},
                "L29": {"power":1.0,"feed":1.0,"color":0xFFDB66},
                "T1":  {"power":0.0,"feed":0.0,"color":0xF36926},
                "T2":  {"power":0.0,"feed":0.0,"color":0x0C96D9}
            }
        }

        return color_table

    def gen_tst_config(self):
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
                         "cut_feed":200,
                         "engrave_power":30.0,
                         "engrave_feed":6000
                         },
             },
        ]

        cfg.append(self.gen_color_table())

        return cfg

    def read(self, name="PythonSCAD.json"):
        name = self.configfile(name)
        with open(name, 'r', encoding='utf-8') as f:
            cfg = json.loads(f.read())
            return cfg
        
    def write(self, config=None, name="PythonSCAD.json"):
        name = self.configfile(name)

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

    def get_machine(self, label=None):
        default = self._config["default"]
        machine = default["machine"]
        head = default["head"]
        print("*** FIXME: default:",default)

        if label is None:
            return default
        else:
            return default[label]

    def set_working(self, default):
        #...
        print("FIXME: not implemented yet.")
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
        print("??? label: '%s'  value: '%s'   dicts: %s"%(label,value,dicts))
        values = [x[value] for x in dicts]
        print("    values:",values)
        return values

    def working_config(self, label="default"):
        ncfg = {}

        dcfg = self.get_sublabel(label,"property")[0]

        lbls = dcfg.keys()

        for l in lbls:
            k = dcfg[l]
            tcfg = self.get_value_by_label(k,"property")
            for i in range(len(tcfg)):
                for tk in tcfg[i].keys():
                    ncfg[tk] = tcfg[i][tk]

        self._working = ncfg
        
        return self._working

    def configfile(self, name="PythonSCAD.json"):
        name = os.path.expanduser(name)
        xdg = os.getenv("XDG_CONFIG_HOME")
        home = os.getenv("HOME")

        if '/'==name[0] or '\\'==name[0]:
            # FIXME: need to also handle 'C:' naming
            return name

        if (xdg is not None) and (os.path.exists(os.path.join(xgd,name))):
            return os.path.join(xgd,name)

        if home is not None:
            return os.path.join(home,".config","PythonSCAD",name)

        return name

    def get_property_value(self, label, tag):
        dicts = [x for x in self._config if x["label"]==label]
        values = [x["property"][tag] for x in dicts]
        return values

    def get_subproperty_value(self, label, tag1, tag2):
        dicts = [x for x in self._config if x["label"]==label]
        values = [x["property"][tag1][tag2] for x in dicts]
        return values

    def set_property_value(self, label, tag, value):
        modified = []
        for d in self._config:
            m = d
            if m["label"]==label:
                if tag in m["property"]:
                    m["property"][tag] = value
            modified.append(m)

        self._config = modified

        return

    def set_subproperty_value(self, label, tag1, tag2, value):
        modified = []
        for d in self._config:
            m = d
            if m["label"]==label:
                if tag1 in m["property"]:
                    m["property"][tag1][tag2] = value
            modified.append(m)

        self._config = modified

        return

    # The followng functions are for manipulating the color table

    def reset_colormap(self):
        """
        reset_colormap: change potentially modified labeled power,
        feed, and color associations back to their default.  The
        default color table is compatible with LightBurn's

        """
        ct = self.gen_color_table()
        modified = []
        for d in self._config:
            if d["label"]=="ColorTable":
                #print(d)
                d["property"] = ct["property"]
            modified.append(d)

        self._config = modified

    def scale_value(self, label1, label2, cfg=None):
        if cfg is None:
            cfg = self._working
        val = cfg[label1] / cfg[label2]
        return val

    def color(self, tag):
        return self.get_subproperty_value("ColorTable", tag, "color")[0]

    # color2str - return the working labled color as an OpenSCAD
    #   compatible string representation of the hex value starting with a
    #   '#'
    def color2str(self, tag):
        return "#{:X}".format(self.color(tag))

    # powermap - return the working labled power
    def power(self, tag):
        return self.get_subproperty_value("ColorTable", tag, "power")[0]

    # feedmap - return the working labled feed
    def feed(self, tag):
        return self.get_subproperty_value("ColorTable", tag, "feed")[0]

    # setpower - overwrite the working labeled power
    def set_power(self, tag, val):
        return self.set_subproperty_value("ColorTable", rag, "power", val)

    # setfeed - overwrite the working labeled feed
    def set_feed(self, key, val):
        return self.set_subproperty_value("ColorTable", rag, "feed", val)

    # setcolor - overwrite the working labeled color
    def set_color(self, key, val):
        return self.set_subproperty_value("ColorTable", rag, "color", val)

    def gen_color(self, red=-1,green=-1,blue=-1,power=-1,feed=-1):
        if (red!=-1 or green!=-1 or blue!=-1) and (power!=-1 or feed!=-1):
            print("Error (gen_color): can only set either RGB or PF values.")
            raise ValueError("Can only set either RGB or PF values.")
        color = 0
        if red   != -1: color |= (int(255.0*red) << 24)
        if green != -1: color |= (int(255.0*green) << 16)
        if blue  != -1: color |= (int(255.0*blue) << 8)
        if power != -1: color |= (int(255.0*power) << 24)
        if feed  != -1: color |= (int(255.0*feed) << 16)

        return color

    def gen_color2str(red=-1,green=-1,blue=-1,power=-1,feed=-1):
        return "#{:X}".format(self.gen_color(red,green,blue,power,feed))

