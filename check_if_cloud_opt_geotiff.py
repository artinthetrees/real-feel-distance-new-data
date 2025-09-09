import subprocess

def geoTiffIsCloudOptimized(geoTiffFilePath):
    #https://www.youtube.com/watch?v=rJ_8na1JY1o

    #out = subprocess.run(["powershell","-c","rio cogeo validate",".\downloads\year2021-month7-day15-hour6-minute0-MRT-mask.tif"],encoding='utf-8',stdout=subprocess.PIPE)
    out = subprocess.run(["powershell","-c","rio cogeo validate",geoTiffFilePath],encoding='utf-8',stdout=subprocess.PIPE)
    print(out)
    if "is a valid cloud optimized GeoTIFF" in str(out):
        return True
    else:
        return False

isCloudOpt = geoTiffIsCloudOptimized("./downloads/year2021-month7-day15-hour10-minute0-MRT-mask.tif")
print("isCloudOpt: ",isCloudOpt)

def convertGeoTiffToCloudOptimized(geoTiffFilePath,outFilePath):
    out = subprocess.run(["powershell","-c","rio cogeo create",geoTiffFilePath,outFilePath],encoding='utf-8',stdout=subprocess.PIPE)
    print(out)

geoTiffFilePath = "./downloads/year2021-month7-day15-hour10-minute0-MRT-mask.tif"
outFilePath = "./downloads/cog-year2021-month7-day15-hour10-minute0-MRT-mask.tif"

isCloudOpt = geoTiffIsCloudOptimized(geoTiffFilePath=geoTiffFilePath)
print("orig file isCloudOpt: ",isCloudOpt)
convertGeoTiffToCloudOptimized(geoTiffFilePath=geoTiffFilePath,outFilePath=outFilePath)
isCloudOpt = geoTiffIsCloudOptimized(geoTiffFilePath=outFilePath)
print("converted file isCloudOpt: ",isCloudOpt)