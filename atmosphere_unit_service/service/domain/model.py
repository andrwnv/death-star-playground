from  service.domain.device import Device

class Model:
    def __init__(self) -> None:
        self.device= {
            "sector 1": Device("Command bridge"),
            "sector 2": Device("Engineering compartment"),
            "sector 3": Device("Crew quarters"),
            "sector 4": Device("Medical bay"),
            "sector 5": Device("Corridors and passageways"),
            "sector 6": Device("Cafeteria"),
            "sector 7": Device("Research laboratory"),
            "sector 8": Device("Alpha storage area"),
            "sector 9": Device("Sigma storage area"),
            "sector 10": Device("Library facilities"),
            "sector 11": Device("Recreation zones"),
            "sector 12": Device("Gardes area"),
            "sector 13": Device("Workbenches"),
            "sector 14": Device("Rest chambers"),
            "sector 15": Device("Lounge area"),
        }
