# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:22:19 2022

@author: Amine
"""

import requests
import json
import pandas as pd
import time
import numpy as np

UUID = "hugJ9hJEkh7yNfBnNLRppThNF1gxBHgG53Va5AQ8T9jahXHv5ZQlOQIx3erNyXliE02fhqhPEpTXRA"
token="RGAPI-1eed7ee5-ddb7-419e-be02-586d23d006df"
headers = {
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": token
    }

def apiToDF(api):
    requete=requests.get(api,headers=headers)
    if requete.status_code !=200:
        print("apiToDF error ",requete)
    requete_json = json.loads(requete.text)
    if (type(requete_json) is dict):
        df = pd.DataFrame.from_dict(requete_json, orient='index')
    else:
        df = pd.DataFrame(requete_json)
    return df

def getUUIDBySummoner(summonerName,tagline):
    api = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/"+summonerName+"/"+tagline
    df = apiToDF(api)
    return df.loc['puuid'][0]

#print(getUUIDBySummoner("Baguetteinlove","EUW"))


def getSummonerByUUID(UUID):
    api = "https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/"+UUID
    df = apiToDF(api)
    gameName = df.loc['gameName'][0]
    return gameName

#UUID_bag = (getUUIDBySummoner("Baguetteinlove","EUW"))


def matchsof(UUID,count,Type):
    
    api = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"+UUID+"/ids?type="+str(Type)+"&start=0&count="+str(count)
    requete=requests.get(api,headers=headers)
    if requete.status_code !=200:
        print("matchsof error ",requete)
    matchs = json.loads(requete.text)
    df_matchs = pd.DataFrame(matchs,columns=['matchs'])
    
    return(df_matchs)
#print(matchsof(UUID_bag,100,'ranked'))

def dfMatch(matchID):
    api = "https://europe.api.riotgames.com/lol/match/v5/matches/"+str(matchID)
    requete=requests.get(api,headers=headers)
    if requete.status_code !=200:
        print("dfMatch error ",requete)
    match = json.loads(requete.text)
    df_match = pd.DataFrame(match)

    return df_match
#df_match = dfMatch("EUW1_5658362841")
#print(df_match)

def dfLadder(division,tier,queue):
    api = "https://euw1.api.riotgames.com/lol/league/v4/entries/"+queue+"/"+tier+"/"+division+"?page=1"
    requete=requests.get(api,headers=headers)
    if requete.status_code !=200:
        print("dfMatch error ",requete)
        print(api)
    ladder = json.loads(requete.text)
    df_ladder = pd.DataFrame(ladder)
    return df_ladder


def getSummoners(matchID):
    df_match = dfMatch(matchID)
    UUIDs = df_match.loc['participants','metadata']
    summoners = []
    for UUID in UUIDs :
        summoners.append(getSummonerByUUID(UUID))
    return summoners, df_match

#summoners = getSummoners("EUW1_5658362841")[0]
#print(summoners)

def getInfo(matchID):
    df_match = dfMatch(matchID)
    df_info = df_match.loc['participants','info']
    return df_info




#df_info = getInfo("EUW1_5658362841")
#print(df_info)

def getStatsBySummonerForMatch(player, matchID):
    summoners, df_match = getSummoners(matchID)
    df_info = df_match.loc['participants','info']
    for k in range (len(summoners)):
        if (summoners[k]==player):
            return df_info[k]
    print("summoner not found in getStatsBySummonerForMatch")
    return "Summoner not found"

def getStatsByUUIDForMatch(UUID,matchID):
    df_match = dfMatch(matchID)
    df_info = df_match.loc['participants','info']
    UUIDs = df_match.loc['participants','metadata']
    for k in range (len(UUIDs)):
        if (UUIDs[k]==UUID):
            return df_info[k]
    print("summoner not found in getStatsBySummonerForMatch")
    return "Summoner not found"

#print(getStatsByUUIDForMatch("hugJ9hJEkh7yNfBnNLRppThNF1gxBHgG53Va5AQ8T9jahXHv5ZQlOQIx3erNyXliE02fhqhPEpTXRA","EUW1_5658362841"))
    
#myStats = getStatsBySummonerForMatch("Baguetteinlove","EUW1_5663768301")
#print(myStats)

def sumName(sumID):
    options = {
        21:"Barrier", 
        1:"Cleanse",
        14:"Ignite",
        3:"Exhaust",
        4:"Flash",
        6:"Ghost",
        7:"Heal",
        11:"Smite",
        12:"Teleport",
        }
    return options.get(sumID,"???")

def analyzeStats(stats):
    role = stats['role']
    championName = stats['championName']
    k = stats["kills"]
    d = stats['deaths']
    a = stats["assists"]
    pinkward = stats['detectorWardsPlaced']
    wardsPlaced = stats['wardsPlaced']
    wardsKilled = stats['wardsKilled']
    mk = stats['largestMultiKill']
    mdmg = stats['magicDamageDealtToChampions']
    pdmg = stats['physicalDamageDealtToChampions']
    tdmg = stats['totalDamageDealtToChampions']
    sums = [stats['summoner1Id'],stats['summoner2Id']]
    usums = [stats['summoner1Casts'],stats['summoner2Casts']]
    heal = stats['totalHeal']
    timePlayed = stats['timePlayed']
    
    kda = (k+0.5*a)/d
    pink_ratio = pinkward/wardsPlaced
    wk_ratio = wardsKilled/wardsPlaced
    mdmg_ratio = mdmg/tdmg
    pdmg_ratio = pdmg/tdmg
    sum1 = [sumName(sums[0]),usums[0]]
    sum2 = [sumName(sums[1]),usums[1]]

    print("role : "+str(role))
    print("championName : "+str(championName))
    print("kda : "+str(round(kda,2)))
    print("pink_ratio : "+str(round(pink_ratio*100))+"%")
    print("wardKill_ratio : "+str(round(wk_ratio*100))+"%")
    print("mdmg_ratio : "+str(round(mdmg_ratio*100))+"%")
    print("pdmg_ratio : "+str(round(pdmg_ratio*100))+"%")
    print("sum1 : "+sum1[0]+",uses : "+str(sum1[1]))
    print("sum2 : "+sum2[0]+", uses : "+str(sum2[1]))
    print("largest multikill : "+str(mk))
    print("total heal : "+str(heal))
    print("temps de jeu : "+str(round(timePlayed/60))+"min")
    
    return [role,championName,kda,pink_ratio,wk_ratio,mdmg_ratio,pdmg_ratio,
            sum1[0],sum1[1],sum2[0],sum2[1],mk,heal,timePlayed]
    
#L = analyzeStats(myStats)
#print(L)

#m = matchsof(getUUIDBySummoner('Aminoquiz','EUW'),5,'ranked')

def getDataFromHistory(summonerName,tagLine,count,t):
    UUID = getUUIDBySummoner(summonerName, tagLine)
    matchList = matchsof(UUID, count, t)
    statsList = []
    for k in range(count):
        time.sleep(0.1)
        print(matchList['matchs'][k])
        stats = getStatsByUUIDForMatch(UUID, matchList['matchs'][k])
        statsList.append(analyzeStats(stats))
    
    return statsList

#liste_stats = getDataFromHistory("Aminoquiz", "EUW", 10, "ranked")

def mostPlayed(statsList):
    champs=[]
    champsCount=[]
    for stats in statsList:
        champ = stats[1]
        if champ not in champs:
            champs.append(stats[1])
            champsCount.append(1)
        else :
            champsCount[champs.index(stats[1])] += 1
    return champs, champsCount

#mostPlayedList = mostPlayed(liste_stats)
#print(str(mostPlayedList[0])+'\n'+str(mostPlayedList[1]))

#print(liste_stats[1][2:7]+liste_stats[1][11:14])

def mostPlayedStats(statsList):
    mostPlayedList,champsCount = mostPlayed(statsList)
    L=[]
    wins = 0
    for i in range(len(mostPlayedList)):
        n = champsCount[i]
        L.append([0,0,0,0,0,0,0,0]) #kda, pink, wardkill, mdmg, pdmg, multikill, heal, timeplayed
    for stats in statsList:
        k = mostPlayedList.index(stats[1])
        M = stats[2:7]+stats[11:14]
        
        L[k]=[L[k][a]+M[a] for a in range(len(M))]
    
    for i in range(len(mostPlayedList)):
        n = champsCount[i]
        print(n)
        L[k]=[L[k][a]/n for a in range(len(L[k]))] #kda, pink, wardkill, mdmg, pdmg, multikill, heal, timeplayed
        
    return L

#meanChamps = mostPlayedStats(liste_stats)
#print(meanChamps)

def mainToText(mostPlayedList,meanChamps):
    for k in range(len(mostPlayedList[0])):
        print("-----"+str(mostPlayedList[0][k])+" played "+str(mostPlayedList[1][k])+" times"+"-----")
        print("kda : "+str(round(meanChamps[k][0],2)))
        print("pink_ratio : "+str(round(meanChamps[k][1]*100))+"%")
        print("wardKill_ratio : "+str(round(meanChamps[k][2]*100))+"%")
        print("mdmg_ratio : "+str(round(meanChamps[k][3]*100))+"%")
        print("pdmg_ratio : "+str(round(meanChamps[k][4]*100))+"%")
        print("largest multikill : "+str(meanChamps[k][5]))
        print("total heal : "+str(meanChamps[k][6]))
        print("temps de jeu : "+str(round(meanChamps[k][7]/60))+"min")
    
    return

###### test = getDataFromHistory("aminoquiz", "EUW", 25, "ranked")
###### print(mainToText(mostPlayedList(test),mostPlayedStats(test)))

df_ladder = dfLadder("I","DIAMOND","RANKED_SOLO_5x5").iloc[1]["summonerName"]

def getTimeline(matchID):
    api = "https://europe.api.riotgames.com/lol/match/v5/matches/"+str(matchID)+"/timeline"
    requete=requests.get(api,headers=headers)
    if requete.status_code !=200:
        print("getTimeline error ",requete)
        print(api)
    timeline = json.loads(requete.text)
    df_timeline = pd.DataFrame(timeline)
    return df_timeline

def getFrames(df_timeline):
    return df_timeline.loc['frames','info']


def getGamesFromLadder(n,m,division,tier):
    """
    

    Parameters
    ----------
    n : int
        nombre de personnes différentes à chercher dans le ladder.
    m : int
        nombre de match par personne.
    division : string
        I,II,III,IV.
    tier : string
        Tier de "IRON", "BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND".

    Returns
    -------
    M : list
        une liste d'identifiants de matchs.

    """
    M = []
    df_ladder = dfLadder(division,tier,"RANKED_SOLO_5x5")
    for i in range(n):
        summonerName = df_ladder.iloc[i]["summonerName"]
        puuid = getUUIDBySummoner(summonerName, "EUW")
        matches = matchsof(puuid,m,"ranked")
        for j in range(m):
            M.append(matches.values.tolist()[j][0])
    return M

mtimeline = getTimeline("EUW1_5745490389")
mframes = getFrames(mtimeline)
minfo = dfMatch("EUW1_5745490389").loc['teams','info']
#faut récup toutes les timeline puis les parcourir de 1 à 10 et compter tous les event 

def teamList(team):
    if team == "blue":
        return [1,2,3,4,5,100]
    return [6,7,8,9,10,200]


def framesToInfos(mID,minutes=10):
    
    mtimeline = getTimeline(mID)
    mframe = getFrames(mtimeline)
    
    result={}
    result['_id']= mID
    if minutes == -1:
        minutes = len(mframe)-1
    for team in ("blue","red"):
        
        ward_placed = []
        ward_kill = []
        skill_level_up=[]
        level_up=[]
        champion_kill=[]
        champion_assist=[]
        champion_special_kill=[]
        elite_monster_kill=[]
        building_kill=[]
        turret_plate_destroyed=[]
        gold_earned=[]
        gold_earned_cum=[]
        minions_killed=[]
        minions_killed_cum=[]

    
        
        for k in range(0,minutes):
            
            f = mframe[k+1]
            
            ward_placed +=[0]
            ward_kill += [0]
            skill_level_up+=[0]
            level_up+=[0]
            champion_kill+=[0]
            champion_assist+=[0]
            champion_special_kill+=[0]
            elite_monster_kill+=[0]
            building_kill+=[0]
            turret_plate_destroyed+=[0]
            gold_earned+=[0]
            minions_killed+=[0]
            gold_earned_cum+=[0]
            minions_killed_cum+=[0]
            
            for e in f['events']:
                if e['type'] == "WARD_PLACED" and (e['creatorId'] in teamList(team) and e['wardType']!='UNDEFINED'):
                    ward_placed[k] = ward_placed[k] + 1
                elif e['type'] == "WARD_KILL" and (e['killerId'] in teamList(team) and e['wardType']!='UNDEFINED'):
                    ward_kill[k] = ward_kill[k] + 1
                elif e['type'] == "SKILL_LEVEL_UP" and (e['participantId'] in teamList(team)):
                    skill_level_up[k] = skill_level_up[k] + 1
                elif e['type'] == "LEVEL_UP" and (e['participantId'] in teamList(team)):
                    level_up[k] = level_up[k] + 1
                elif e['type'] == "CHAMPION_KILL" and (e['killerId'] in teamList(team)):
                    champion_kill[k] = champion_kill[k] + 1
                    # print(e['killerId'])
                    # print("----->>>>>"+team+"<<<<<<-----")
                    # print("----->>>>>"+str(teamList(team))+"<<<<<<-----")
                    #print(e)
                    if 'assistingParticipantIds' in e:
                        for assist in (e['assistingParticipantIds']):
                            champion_assist[k] = champion_assist[k]+1
                
                elif e['type'] == "CHAMPION_SPECIAL_KILL" and (e['killerId'] in teamList(team)):
                    champion_special_kill[k] = champion_special_kill[k]+1
                    # print("----->>>>>"+team+"<<<<<<-----")
                    # print(e)
                    
                elif e['type'] == "ELITE_MONSTER_KILL" and (e['killerId'] in teamList(team)):
                    elite_monster_kill[k] = elite_monster_kill[k]+1

                elif e['type'] == 'BUILDING_KILL' and (e['teamId'] not in teamList(team)) :
                    building_kill[k] = building_kill[k]+1
                    # print(e)
                    # print("----->>>>>"+team+"<<<<<<-----")
                    # print(e['teamId'])
                
                elif e['type'] == 'TURRET_PLATE_DESTROYED' and (e['teamId'] not in teamList(team)):
                    turret_plate_destroyed[k] = turret_plate_destroyed[k]+1

                elif e['type'] == "GAME_END":
                    print("----->>>>>"+team+"<<<<<<-----")
                    # print(e)
            
            for n in teamList(team)[0:5]:
                pf=f['participantFrames'][str(n)]

                gold_earned_cum[k]=gold_earned_cum[k]+pf['totalGold']
                minions_killed_cum[k]=minions_killed_cum[k]+pf['minionsKilled']+pf['jungleMinionsKilled']
            if k>0:
                gold_earned[k] = gold_earned_cum[k]-gold_earned_cum[k-1]
                minions_killed[k]= minions_killed_cum[k]-minions_killed_cum[k-1]
            else:
                gold_earned[0]=2500
                
        # print('ward_placed : '+str(ward_placed)+' sum :'+str(sum(ward_placed)))
        # print('ward_kill : '+str(ward_kill)+' sum :'+str(sum(ward_kill)))
        # print('champion_kill : '+str(champion_kill)+' sum :'+str(sum(champion_kill)))
        # print('champion_assist : '+str(champion_assist)+' sum :'+str(sum(champion_assist)))
        # print('champion_special_kill : '+str(champion_special_kill)+' sum :'+str(sum(champion_special_kill)))
        # print('elite_monster_kill : '+str(elite_monster_kill)+' sum :'+str(sum(elite_monster_kill)))
        # print('building_kill : '+str(building_kill)+' sum :'+str(sum(building_kill)))
        # print('turret_plate_destroyed : '+str(turret_plate_destroyed)+' sum :'+str(sum(turret_plate_destroyed)))
        # print('gold_earned : '+str(gold_earned)+' sum :'+str(sum(gold_earned)))
        # print('minions_killed : '+str(minions_killed)+' sum :'+str(sum(minions_killed)))
        
        result[str(team)+'_'+'ward_placed'] = (ward_placed)
        result[str(team)+'_'+'ward_kill'] = (ward_kill)
        result[str(team)+'_'+'level_up'] = (level_up)
        result[str(team)+'_'+'champion_kill'] = (champion_kill)
        result[str(team)+'_'+'champion_assist'] = (champion_assist)
        result[str(team)+'_'+'champion_special_kill'] = (champion_special_kill)
        result[str(team)+'_'+'elite_monster_kill'] = (elite_monster_kill)
        result[str(team)+'_'+'building_kill'] = (building_kill)
        result[str(team)+'_'+'turret_plate_destroyed'] = (turret_plate_destroyed)
        result[str(team)+'_'+'gold_earned'] = (gold_earned)
        result[str(team)+'_'+'minions_killed'] = (minions_killed)
        
        
        # result = result+[sum(ward_kill)]
        # result = result+[sum(level_up)]
        # result = result+[sum(champion_kill)]
        # result = result+[sum(champion_assist)]
        # result = result+[sum(champion_special_kill)]
        # result = result+[sum(elite_monster_kill)]
        # result = result+[sum(building_kill)]
        # result = result+[sum(turret_plate_destroyed)]
        # result = result+[sum(gold_earned)]
        # result = result+[sum(minions_killed)]
        
    return result

R = framesToInfos("EUW1_5745490389", -1)

#plein_de_matchs = getGamesFromLadder(10,5,"I","DIAMOND")

plein_de_matchs2 = matchsof(getUUIDBySummoner('Aminoquiz','EUW'),10,'ranked')

res = {}
for k in range(len(plein_de_matchs2)):
    mID = plein_de_matchs2.loc[k,'matchs']
    print(mID)
    res[mID] = framesToInfos(mID,-1)



    

 