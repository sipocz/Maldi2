
import os
import shutil
import datetime as dt
import re
''' GLOBAL
'''
_DirectoryIn="C:/Space/maldi2/IN"
_DirectoryResult="C:/Space/maldi2/RESULT"
_DirectoryOut="C:/Space/maldi2/OUT2"
_DebugToFile=True
_logprefix = "C:/Space/maldi2/log"
_logext = ".log"
_swname = "MALDI"
_ResultEnd = "_RESULT_X"

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
        for r, d, f in os.walk(folder):
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
    if msgstr=="":
        caller=sys._getframe(1).f_code.co_name
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
            print("\t\t"+msgstr,file=fname)
            fname.close()
        else:
            print("\t\t" + msgstr)


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






def saveCSVfile(a, fname):
    csvfile = open(fname, "w",encoding='utf-8-sig')
    for i in a:
        s = ""
        for j in i:
            s = s + str(j) + ";"

        #print(s[0:-1])
        csvfile.writelines(s[0:-1] + "\n")
    csvfile.close()

def loadCSVfile(fname):
    '''
    csv fálj betöltése egy listába
    param fname: a fájl neve teljes elérési út
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
    '''
    import datetime as dt
    from os import path as ospath

    currentdate=dt.datetime.now()
    isostr=currentdate.isoformat()
    datestr="/"+_swname+str(isostr[0:4])+str(isostr[5:7])+str(isostr[8:10])
    fname=_logprefix+datestr+_logext
    #print(fname)
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
    return([parts[2],parts[3],fname])


def splitOutfiles(fnamelist):
    '''
    :param fnamelist: a könyvtár fájljai listába szedve
    :return:  teljes listát generál a kulccsal
    '''
    out=[]
    for fname in fnamelist:
        out.append(splitOutfile(fname))
    return(out)

def splitInfile(fname):
    '''
    :param fname: szétkapja a MALDI INPUT file nevet
    :return:  a kulcs és a fájl neve listában
    '''
    fname_list=fname.split(".")
    fname_1=fname_list[0]
    parts=fname_1.split("-",1)
    return([parts[0],parts[1],fname])

def splitInfiles(fnamelist):
    '''
    :param fnamelist: a könyvtár fájljai listába szedve
    :return:  teljes listát generál a kulccsal
    '''
    out=[]
    for fname in fnamelist:
        out.append(splitInfile(fname))
    return(out)

def listoutfiles():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(_DirectoryOut):
        f.extend(filenames)
    return(f)

def listinfiles():
    f = []
    for (dirpath, dirnames, filenames) in os.walk(_DirectoryIn):
        f.extend(filenames)
    return(f)



def findMatchInOutFile():
    out={}
    inlist=listinfiles()
    outlist=listoutfiles()
    #print(inlist)
    #print(outlist)
    msg(tofile=_DebugToFile)
    for infile in inlist:
        for outfile in outlist:
            if (splitInfile(infile)[0] in splitOutfile(outfile)[0]) and (splitInfile(infile)[1] in splitOutfile(outfile)[1]):
                msg("match:  "+infile+" _AND_  "+outfile,tofile=_DebugToFile)
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
    :param key: a kulcsot
    :param list:  a lista
    :param column: ebben a listaelemben keres
    :return: a lsita sora, ha megtaláltuk kúlönben None
    '''
    for line in list:
        #print("line:",line)
        if line[column]==key:
            return(line)
        else:
            pass
    return (None)

def writeResultFile(fname,reslist):
    '''
    Létrehozza az eredményfájlt
    :param fname: a készítendő file neve, a könyvtárnévvel automatikusan kiegészítésre kerül
    :param reslist: lista a file elemeiről
    :return:  None
    '''
    fname=_DirectoryResult+"/"+fname
    f=open(fname,"w")
    for line in reslist:
        for field in line:
            print(field+";",end="",file=f)
        print("",file=f)
    f.close()


def runacheck():
    matched=findMatchInOutFile()
    for afile in matched:
        #print(afile)
        sfileok = False
        ffileok = False
        for outfiles in matched[afile]:
            #print(outfiles)
            #print("--------------------------")
            #print(re.match(r'[0-9_-]*f[0-9_ -]*.csv', outfiles))
            if re.match(r'[0-9_-]*s[0-9_ -]*.csv', outfiles):
                sfilename = _DirectoryOut + "/" + outfiles
                sfileok=True
                #print(sfilename)
            if re.match(r'[0-9_-]*f[0-9_ -]*.csv', outfiles):
                ffilename = _DirectoryOut + "/" + outfiles
                ffileok=True

        infile=loadCSVfile(_DirectoryIn+"/"+afile)
        if sfileok:
            sfile=loadCSVfile(sfilename)
        if  ffileok:
            ffile=loadCSVfile(ffilename)
        #print(infile)
        #print(sfile)
        #print(ffile)
        infile=loadCSVfile(_DirectoryIn+"/"+afile)
        #print(infile)
        #print("----------------------")
        resultlist=[]
        for line in infile:
            id=line[1]
            #print(id)
            #check in f file
            #print(id)
            frow=checkInLine(id,ffile,0)
            srow=checkInLine(id,sfile,0)
            if frow==None :
                #print(srow)
                result=srow
            else:
                #print(frow)
                result=frow
            resultlist.append([id,result[3],result[6]])
        resultfilename=createResultFileName(afile)
        #print(resultfilename)
        #print(resultlist)
        writeResultFile(resultfilename,resultlist)




'''
 MAIN
'''

msg(tofile=_DebugToFile)
msg("MALDI Converter Started",tofile=_DebugToFile)
filename="1011026779-2020-07-28 14-22-26.csv"

fin_name=_DirectoryIn+"/"+filename
fin=loadCSVfile(fin_name)
#print(fin)

'''
    for f in fin:
        print(f[1])
    
    print("-------------------------------------------------------------------------------")
  '''

filename="20200811-1501-1011026779s-2020-08-11 14-28-46.csv"
fout_name=_DirectoryOut+"/"+filename
fout=loadCSVfile(fout_name)
#print(fout)
'''
for f in fout:
    print(f[0])
  '''
for codein in fin:
    for codeout in fout:
        if codein[1]==codeout[0]:
            print(codein[1],";",codeout[3],";",codeout[6], sep="")
outfiles=listoutfiles()
#print(splitOutfiles(outfiles))
outfiles=listinfiles()
#print(splitInfiles(outfiles))


findMatchInOutFile()
#print("*******************")
runacheck()
