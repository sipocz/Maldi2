# +----------------------------------------
# |  Maldiconverter   
# | 
# |  Sipőcz László   
# |  1.0: 2020.10.01. Maldiconverte
# |         Maldi eredmények visszaadása MIMOLAB fele
# |  
# |  2.0: 2020.02.05.  (Validált verzió) 
# |         Backup könyvtárakba siteonként mentés  
# |         Területenként összesített adatok készítése
# |           
# +----------------------------------------

import os
import shutil
import datetime as dt
import re

currentyear="Y_"+str(dt.datetime.now().year)

'''
GLOBAL CONSTANT definitions
'''

state="DEV"             # <-- fejlesztési állapot  
_pathprefix="C:\\"      # <--   hálózati környezetben "\\\\" !!   


_logext = ".log"
_swname = "MALDI_Converter_"
_ResultEnd = "_RESULT"
_site_kezi_dir_End="_kezi"
_site_allfile_prefix="!"
_site_allfile_postfix="_all"


'''
DIRECTORY definitions
'''


_Basedirectory="C:\\Maldi\\Maldi2-master"

_Backupdirectory=_pathprefix+"hungary\dfsroot\\Maldi_Backups\\"+state            # 2021.02.03
_Backupdirectory_root=_pathprefix+"hungary\dfsroot\\Maldi_Backups"             # 2021.02.04

# -----------------------------------------------------------------------------------
_Indirectory=_pathprefix+"hungary\\dfsroot\\Maldi_eredmenyek\\"+state+"\\MALDI_INPUT"
_Resultdirectory=_pathprefix+"hungary\\dfsroot\\Maldi_eredmenyek\\"+state+"\\MIMOLAB" #"/RESULT"

#------------------------------------------------------------------------------------
_Outdirectory="\\MaldiOut"
_Logdirectory="\\log"

_UsedPlateFile="plates.dat"


_DirectoryIn=_Indirectory
_DirectoryResult=_Resultdirectory
_DirectoryOut="C:"+_Outdirectory
_DebugToFile=True
_logprefix = _Basedirectory+_Logdirectory


_usedplatelist=_Basedirectory+"\\"+_UsedPlateFile    # egy fájlra mutat ami csv-ként tartalmazza a plateID és fióktelep összerendeléseket



def searchfiles(outFileName, extension='.ttf', folder='C:\\', deltaTime=3600 * 24):
    """
    ***************************
    Listát készít egy adott könyvtárban lévő megadott kiterjesztésű fájlokból rekurzívan.
    A listát eltárolja a outFileName -ban megadott helyre
    Csak azokat a fájlokat veszi figyelembe, amelyek kora kisebb mint a megadott idő [sec]
    ***************************
    :param outFileName:     ide menti a kimeneti listát
    :param extension:       ezeket a fájlokat keresi
    :param folder:          ebben a könyvtárban keres
    :param deltaTime:       ilyen korú, vagy fiatalabb fájlokat keresi [sec]-ben kell megadni!!
    :return: ---
    """
    "Create a txt file with all the file of a type"
    currentDateTimeStamp = dt.datetime.now().timestamp()
    # print (currentDateTimeStamp)
    with open(outFileName, "w", encoding="utf-8") as filewrite:
        for r, _, f in os.walk(folder):
            for file in f:
                if file.endswith(extension):
                    # print(r+file)
                    fname = r + "\\" + file
                    fileTimeStamp = os.path.getctime(fname)
                    # print(fileTimeStamp)
                    if (currentDateTimeStamp - fileTimeStamp) <= deltaTime: 
                        filewrite.write(f"{fname}\n")


def timestamp(): 
    '''
    Az aktuális időpontot adja vissza string formában YYYY-MM-DD HH-MM-SS.xxxxxx
    '''
    n = dt.datetime.now()
    n.isoformat(" ", "seconds")
    # print(n)
    return (n)


def msg(msgstr="",tofile=True):
    '''
    :param msgstr: kiírandó szöveg
    :param tofile: alapértelmezett True esetén fájba ír, átírva standard kimenet
    :return:
    '''
    import sys
    caller=sys._getframe(1).f_code.co_name
    if msgstr=="":
        
        if tofile:

            filename=createLogFile()
            fname=open(filename, "a")
            print(timestamp(),file=fname)
            print("\tDEF: ",caller,file=fname)
            fname.close()
        else:
            print(timestamp())
            print("\tDEF: ", caller)
        #print("~"*(len(caller)+4))
    else:
        if tofile:
            filename = createLogFile()
            fname=open(filename, "a")
            print("\t\t"+caller+"-"+msgstr,file=fname)
            fname.close()
        else:
            print("\t\t" +caller+"-"+msgstr)


def parseCSV(str):
    '''
    pontosvessző tagolt stringet elemei bont 
    :param str: a feldolgozandó string  
    :return:  list
    '''
    # print("parse:", str.strip())

    a = str.strip().split(";")
    return (a)

#e8 = u.encode('utf-8')        # encode without BOM
#e8s = u.encode('utf-8-sig')   # encode with BOM
#e16 = u.encode('utf-16')      # encode with BOM
#e16le = u.encode('utf-16le')  # encode without BOM
#e16be = u.encode('utf-16be')  # encode without BOM


def loadCSVfile(fname):
    '''
    csv fálj betöltése egy listába
    param fname: a fájl neve teljes elérési út
    :return: listában adja vissza a file tartalmát
    '''
    msg()
    msg("filename:"+fname)
    l1=[]
    csvfile = open(fname, "rt" , encoding='latin-1')
    for line in csvfile.readlines():
        l1.append(parseCSV(line))
    csvfile.close()
    return (l1)


def createLogFile():
    '''
    meghatározza a msg fájl nevét
    :return: a Log file neve stringként
    '''
    import datetime as dt
    from os import path as ospath
    currentdate=dt.datetime.now()
    isostr=currentdate.isoformat()
    datestr="\\"+_swname+str(isostr[0:4])+str(isostr[5:7])+str(isostr[8:10])
    fname=_logprefix+datestr+_logext
    #print(fnamep
    if ospath.exists(fname):
       pass
    else:
        fileLog = open(fname, "x")
        fileLog.close()
        msg(tofile=_DebugToFile)
        msg("created",tofile=_DebugToFile)
    return (fname)


def createResultFileName(filename):
    '''
    A kimeneti fájl nevét generálja
    :param filename:  az input fájl neve
    :return: string a result file neve NEM tartalmazza a teljes elérési utat
    '''
    msg( tofile=_DebugToFile)
    fname=filename.split(".")
    ext=fname[-1]
    if  ext!="csv":
        return()
    out=fname[0]+_ResultEnd+"."+"csv"
    msg("RESULT file name created:"+out)
    return(out)


def splitOutfile(fname):
    '''
    :param fname: szétkapja a MALDI OUT file nevet
    :return:  a kulcs és a fájl neve listában
    '''
    fname_list=fname.split(".")
    fname_1=fname_list[0]
    parts=fname_1.split("-",3)
    print(parts)
    return([parts[2],parts[3],fname])


def splitOutfiles(fnamelist):
    '''
    :param fnamelist: a könyvtár fájljai listába szedve
    :return:  teljes listát generál a kulccsal
    '''
    msg(tofile=_DebugToFile)
    out=[]
    for fname in fnamelist:
        out.append(splitOutfile(fname))
    msg("return: "+str(out), tofile=_DebugToFile)
    return(out)


def splitInfile(fname):
    '''
    :param fname: szétkapja a MALDI INPUT file nevet
    :return:  a kulcs és a fájl neve listában
    '''
    msg("",tofile=_DebugToFile)
    fname_list=fname.split(".")
    fname_1=fname_list[0]
    parts=fname_1.split("-",1)
    print(fname)
    print(parts)
    msg("return a split: "+str([parts[0],parts[1],fname]), tofile=_DebugToFile)
    return([parts[0],parts[1],fname])


def splitInfiles(fnamelist):
    '''
    :param fnamelist: a könyvtár fájljai listába szedve
    :return:  teljes listát generál a kulccsal
    '''
    msg(tofile=_DebugToFile)
    out=[]
    for fname in fnamelist:
        out.append(splitInfile(fname))
    msg("return: "+str(out), tofile=_DebugToFile)
    return(out)


def listoutfiles():
    '''
    OUT könyvtár elemeit listázza
    :return: listába rendezett fálnevek
    '''
    print("listoutfile: ", _DirectoryOut)
    msg(tofile=_DebugToFile)
    f = []
    for (_, _, filenames) in os.walk(_DirectoryOut):
        f.extend(filenames)
    msg("return: "+str(f), tofile=_DebugToFile)
    return(f)


def listinfiles():
    '''
    IN könyvtár elemeit listázza
    :return: listába rendezett fálnevek
    '''
    print("listinfile: ", _DirectoryIn)
    msg(tofile=_DebugToFile)
    f = []
    for  (_, _, filenames) in os.walk(_DirectoryIn):
        f.extend(filenames)
    msg("return: "+str(f), tofile=_DebugToFile)
    return(f)



def findMatchInOutFile():
    '''
    név alapján összekapcsolja az IN és OUT könyvtárban lévő fájlokat
    :return: listában adja vissza az egymáshoz tartozó fájlokat
    '''
    out={}
    inlist=listinfiles()
    outlist=listoutfiles()
    #print(inlist)
    #print(outlist)
    msg(tofile=_DebugToFile)
    for infile in inlist:
        for outfile in outlist:
            if (splitInfile(infile)[0] in splitOutfile(outfile)[0]) and (splitInfile(infile)[1] in splitOutfile(outfile)[1]):
                msg("match:  "+infile+" _AND_ "+outfile,tofile=_DebugToFile)
                # tároljuk be az infókat
                if infile not in out:
                    out[infile]=[outfile]
                else:
                    out[infile].append(outfile)
    msg("return: "+str(out), tofile=_DebugToFile)
    return(out)

def findMatchedInOutFile():
    '''
    név alapján összekapcsolja az IN és OUT könyvtárban lévő fájlokat
    1-1 megfeleltetés a végleges megoldáshoz 
    :return: listában adja vissza az egymáshoz tartozó fájlokat
    '''
    out={}
    inlist=listinfiles()
    outlist=listoutfiles()
    print(inlist)
    print(outlist)
    msg(tofile=_DebugToFile)
    for infile in inlist:
        for outfile in outlist:
            if (splitInfile(infile)[0] in splitOutfile(outfile)[0]) and (splitInfile(infile)[1] in splitOutfile(outfile)[1]):
                msg("match:  "+infile+" _AND_ "+outfile,tofile=_DebugToFile)
                # tároljuk be az infókat
                if infile not in out:
                    out[infile]=[outfile]
                else:
                    out[infile].append(outfile)
    msg("return: "+str(out), tofile=_DebugToFile)
    return(out)

def checkInLine(key, list,column):
    '''
    kulcsot keres egy listában
    :param key: a kulcs
    :param list:  a lista
    :param column: ebben a listaelemben keres
    :return: a lista sora, ha megtaláltuk kúlönben None
    '''
    for line in list:
        #print("line:",line)
        if line[column]==key:
            return(line)
        else:
            pass
    return (None)


def writeResultFile(fnamein,reslist):
    '''
    Létrehozza az eredményfájlt
    :param fnamein: a készítendő file neve, a könyvtárnévvel automatikusan kiegészítésre kerül
    :param reslist: lista a file elemeiről
    :return:  None
    '''
    fname=_DirectoryResult+"\\"+fnamein
    f=open(fname,"w")
    for line in reslist:
        for field in line:
            print(field+";",end="",file=f)
        print("",file=f)
    f.close()

def writeManualResultFile(Directory,fnamein,reslist):
    '''
    Létrehozza az eredményfájlt
    :param fnamein: a készítendő file neve, a könyvtárnévvel automatikusan kiegészítésre kerül
    :param reslist: lista a file elemeiről
    :return:  None
    '''
    msg(tofile=_DebugToFile)
    print("Directory:",Directory)
    fname=Directory+"\\"+fnamein
    print("Fname:",fname)
    f=open(fname,"w", encoding="Latin")  # latin van itt, 
    for line in reslist:
        for field in line:
            if field!=line[-1]:
                print(field+";",end="",file=f)
            else:
                print(field,end="",file=f)
        
        print("",file=f)
    f.close()

def loadplates():
    '''
    A plate azonosítókat tartalmazó fájl beolvasása
    dictionary lesz, amit a plateID indexel!
    return: dictionary
    '''
    msg(tofile=_DebugToFile)
    try:
        f=loadCSVfile(_usedplatelist)
        f2=dict(f)
        return(f2) 
    except:
        msg("Hiba a file olvasásban: "+_usedplatelist,tofile=_DebugToFile)


def moveafile(sourceFile,destpath):
    '''
    A fájlog átmozgatását végzi, hibakezeléssel 
    return: null
    '''
    msg(tofile=_DebugToFile)
    try:
        shutil.move(sourceFile,destpath) 
        msg("file:"+sourceFile+" dest:"+destpath,tofile=_DebugToFile)
    except:
        msg("hiba a file átmozgatásban:"+sourceFile+" dest:"+destpath,tofile=_DebugToFile)
    return(0)

def copyafile(sourceFile,destpath):
    '''
    A fájlog átmásolását végzi, hibakezeléssel 
    return: null
    '''
    msg(tofile=_DebugToFile)
    try:
        shutil.copy(sourceFile,destpath) 
        msg("file:"+sourceFile+" dest:"+destpath,tofile=_DebugToFile)
    except:
        msg("hiba a file átmásolásban:"+sourceFile+" dest:"+destpath,tofile=_DebugToFile)
    return(0)



def file_append(basefile,appender,toppos=True):
    msg(tofile=_DebugToFile)
    tmp_ext="_tmp"
    if os.path.isfile(basefile):
        pass
    else:
        writeManualResultFile(os.path.dirname(basefile),os.path.basename(basefile),[])   
    base1=loadCSVfile(basefile)
    app1=loadCSVfile(appender)
    if toppos:
        o_list=app1+base1
    else:
        o_list=base1+app1
    writeManualResultFile(os.path.dirname(basefile),os.path.basename(basefile),o_list)

    
    



def runthecheck():
    '''
    Elvégezzük az ellenőrzést
    1-1 megfeleltetés van az input és az output file között
    legeneráljuk a Mimolab fele az eredményfájlt
    legeneráljuk a kézi eredményfájlokat
    összesített listát készítünk
    backupoljuk az adatokat a megfelelő könyvtárakba
    rendet rakunk magunk után

    '''
    msg(tofile=_DebugToFile)
    matched=findMatchedInOutFile()
    if len(matched)==0:
        msg("No Match Found: ", tofile=_DebugToFile)
        print("kilépés")
        return  # nincs mit csinálni
    print ( matched)
    for afile in matched:
        print("afile:",afile)
        msg("file:"+afile,tofile=_DebugToFile)
        #print(matched[afile])
        outfile = matched[afile][0]
        #print(outfile)
            #print("--------------------------")
            #print(re.match(r'[0-9_-]*f[0-9_ -]*.csv', outfiles))
            
        infilename=_DirectoryIn+"\\"+afile
        infile=loadCSVfile(infilename)
        outfilename=_DirectoryOut+"\\"+outfile
        outfile=loadCSVfile(outfilename)
        
        print("----------------------")
        resultlist=[]
        for line in infile:
            #print("line: ", line)
            id=line[1]
           
            result=checkInLine(id,outfile,0)
            #print("result:", result)
            resultlist.append([id,result[3],result[6]])
            #print("eddig eljutottunk")
        resultfilename=createResultFileName(afile)
        
        # A mimolab fele csak az "ID"-t tartalmazó fájlok mennek vissza
        
        # --------------------------------------------------------
        # |                       2021.02.02.
        # | A mimolab fele csak az "ID"-t tartalmazó fájlok mennek vissza
        # |
        # -------------------------------------------------------- 
        if "ID" in resultfilename:
            writeResultFile(resultfilename,resultlist)
            # ----------------------------------------------------
            #   még a ID-t tartalmazó fájlokat is backupolni kell külön
            #   ide fognak kerülni 
            #   pl.: \\hungary\dfsroot\maldi_backups\prd\MIMOLAB\Debrecen_kezi\Y_2021
            #   
            # ----------------------------------------------------
            for plate in plates:
                if plate in infilename:                                         # megtaláltuk a plate azonosítót
                    selectedsite=plates[plate]                                  # ez a site neve
                    # pl.: \\hungary\dfsroot\maldi_backups\prd\Debrecen_kezi\Y_2021
                    destpath=_Backupdirectory_root+"\\"+state+"\\"+"MIMOLAB"+"\\"+selectedsite+"\\"+currentyear                 # ez a backup könyvtár neve site névvel kiegészítve
                    writeManualResultFile(destpath,resultfilename,resultlist)   # resultfile létrehozása ide is
                    
                    copyafile(infilename,destpath)                              # infile másolása #20210208 move -> copy 
                    copyafile(outfilename,destpath)                             # outfile másolása #20210208 move -> copy
                    pdfname=outfilename[:-3]+"pdf"
                    copyafile(pdfname,destpath)                                 # pdf másolása  #20210208 move -> copy  
                    
                    # MIMOLAB fele menő adatokat nem rakunk ott össze mert ezek megjelennek a site adatai között 
                     
                    
        
        # +-------------------------------------------------------
        # |             itt szedjük össze az adatokat
        # |                       2021.02.02
        # |  plates.dat id-t keresünk az Infile nevébenban
        # |  ha megtaláltuk akkor infile-t, outfile-t átmásoljuk
        # |  result fájlt legeneráljuk  a backup könyvtárba
        # |  az alkönyvtár a plates.dat-ban található site által meghatározott 
        # |  alkönyvtárába kerül
        # |  Még össze is kell rakni az összesített .csv listáját ez nem egyenlő a mimolab 
        # |  RESULT fájl-lal.
        # +------------------------------------------------------- 
        for plate in plates:
            if plate in infilename:                                         # megtaláltuk a plate azonosítót
                selectedsite=plates[plate]                                  # ez a site neve
                # pl.: \\hungary\dfsroot\maldi_backups\prd\Debrecen_kezi\Y_2021
                destpath=_Backupdirectory+"\\"+selectedsite+_site_kezi_dir_End+"\\"+currentyear                 # ez a backup könyvtár neve site névvel kiegészítve
                moveafile(infilename,destpath)                              # infile másolása
                moveafile(outfilename,destpath)                             # outfile másolása
                pdfname=outfilename[:-3]+"pdf"
                moveafile(pdfname,destpath)                                 # pdf másolása    
                writeManualResultFile(destpath,resultfilename,resultlist)   # resultfile létrehozása ide is
                # készen is lennénk de még össze kell állítani az összesített listát
                # az adatok az infile és outfile listában vannak
                Sumlist=[]
                for line in infile:
                    #print("line: ", line)
                    position=line[0]
                    plateID=line[1]
                    nameanddate=line[2]
                    try:
                        # ha nincs kitöltve a dátum akkor még ne adjuk fel 
                        Name_hely=nameanddate.split("#")[0]
                        Name_datum=nameanddate.split("#")[1]
                    except:
                        msg("Hiba a descriptor szeletelésben ", tofile=_DebugToFile)
                        Name_datum="99991231"
                        Name_hely=nameanddate
                    Name_datum=Name_datum[0:4]+"."+Name_datum[4:6]+"."+Name_datum[6:]   # átalakítjuk a dátumot a magyar helyesírás szerintire 

                    sampleType=line[3]
                    PrepProt=line[4]
                    Description=line[5]

           
                    result=checkInLine(plateID,outfile,0)
                    detected=result[3]
                    logscore=result[6]
                    #print("result:", result)
                    Sumlist.append([Name_hely,Name_datum,plateID,Description,sampleType,PrepProt,detected,logscore])
                    #print("eddig eljutottunk")
                # ha eddig eljutottunk, akkor a Sumlist -ben vannak az adatok 
                # ki kell írni CSV-be a 
                writeManualResultFile(destpath,"Sum"+afile,Sumlist)
                # hozzá kell írni a alldata file-hoz!!!
                alldatafile=_Backupdirectory+"\\"+selectedsite+_site_kezi_dir_End+"\\"+currentyear+"\\"+_site_allfile_prefix+selectedsite+_site_allfile_postfix+".csv"
                additionalfile=destpath+"\\"+"Sum"+afile
                print("alldata :", alldatafile)
                print("additional :", additionalfile)
                

                file_append(alldatafile,additionalfile)




        #--------------------------------------------------------
        
        #print(infilename,_BackupIN)
        #shutil.move(infilename,_BackupIN)    
        #result file backup
        resultfilefullname=_DirectoryResult+"\\"+resultfilename
        #shutil.move(resultfilefullname,_Backupresult) 

         
        
'''
 MAIN
'''
msg(tofile=_DebugToFile)


msg("MALDI Converter Start",tofile=_DebugToFile)
plates=loadplates()
runthecheck()  
msg("MALDI Converter End",tofile=_DebugToFile)
