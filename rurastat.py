#!/env/python

import sys,io,argparse,glob,hashlib,os
try:
    import plotly.plotly as py
    import plotly.graph_objs as go
    plotly_enabled = True
except: plotly_enabled=False
"""
  rurastat.py 1.0
    author: Dimitri Fousekis (@rurapenthe0)
    Licensed under the GNU General Public License Version 2 (GNU GPL v2),
        available at: http://www.gnu.org/licenses/gpl-2.0.txt
    (C) 2018 Dimitri Fousekis (@rurapenthe0)
    TODO:
    Please send a tweet to @rurapenthe0 with any suggestions or comments.

"""

cmdparams = argparse.ArgumentParser(description="RuraStat - Check found passwords against your wordlists and see statistics")
cmdparams.add_argument("-f", help="File containing found/cracked passwords 'Founds' as input",action="store",dest="fileinput", required=True)
cmdparams.add_argument("-d", help="Directory containing wordlists to be scanned",action="store",dest="filedir", required=True)
cmdparams.add_argument("-r", help="Raw output only, no headers and other info", action="store_true", dest="rawonly", default=False)
if plotly_enabled: cmdparams.add_argument("-p", help="Output statistics graph to Plotly", action="store_true", dest="plot_graph", default=False)

args = cmdparams.parse_args()

def getFilesfromDir(directorypath):
    return glob.glob(directorypath+'/*', recursive=True)

def inputWordHashlist(inputfile):
    words_in=[]
    hasher = hashlib.md5()
    for wordInput in open(inputfile,encoding='utf-8'):
       words_in.append(wordInput.rstrip())


    return words_in

def returnHitCount(inputwords,wordlistfile):
    hitcount = 0

    for candidates in open(wordlistfile,encoding='utf-8'):
       if candidates.rstrip() in inputwords: hitcount+=1

    return hitcount

def main():
    statsDict = {}
    show = """
       ___                ______       __    ___ ___
  / _ \__ _________ _/ __/ /____ _/ /_  <  // _ \
 / , _/ // / __/ _ `/\ \/ __/ _ `/ __/  / // // /
/_/|_|\_,_/_/  \_,_/___/\__/\_,_/\__/  /_(_)___/"""
    print(show)
    print ("RuraStat, a tool to check for found passwords in your wordlists and show hit statistics")
    print ("")
    print ("[+] Loading input candidates from your found list...")

    try:
        inputCandidates = inputWordHashlist(args.fileinput)
    except IOError as error:
        print("[-] Error while reading input file")
        print(error)
        sys.exit(-1)

    print ("[+] OK, Loaded "+str(len(inputCandidates)) + " cracked passwords / 'Founds' to check.")
    try:
        fileList = getFilesfromDir(args.filedir)
    except IOError as error:
        print("[-] Error while getting directory listing of your wordlists")
        print (error)
        sys.exit(-1)

    print ("[+] OK, loaded "+str(len(fileList))+" wordlist files to look for 'Founds'.")
    print ("[+] Building statistics...")
    for files in fileList:
        statsDict[os.path.basename(files)] =  returnHitCount(inputCandidates,files)
    print ("[+] Scan complete....")
    print ("-------------------------------------------------------------------------------")
    print ("")
    for keys,values in statsDict.items():
        print ("Wordlist: "+keys+" | Number of 'Founds' in this file: "+str(values))

    print ("-------------------------------------------------------------------------------")
    if args.plot_graph:
            print ("[+] You have enabled Plotly and chose to output to Plotly graph. Press a key to output now...")
            xx = []
            yy= []
            for keys,values in statsDict.items():
              xx.append(keys)
              yy.append(values)
            trace = go.Bar(x=xx,y=yy)
            data = [ trace ]
            py.plot(data)

    print ("[+] All done!")
    sys.exit(0)


if __name__ == "__main__":
	main()






