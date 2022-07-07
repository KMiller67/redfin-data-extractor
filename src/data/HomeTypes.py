from enum import Enum


class HomeTypes(Enum):
    HOUSE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[1]/div'
    TOWNHOUSE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[2]/div'
    CONDO = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[3]/div'
    LAND = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[4]/div'
    MULTIFAMILY = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[5]/div'
    MOBILE = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[6]/div'
    COOP = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[7]/div'
    OTHER = '//*[@id="filterContent"]/div/div[5]/div[2]/div/div/div/div/div[8]/div'
