# Library
from collections import Counter
import itertools as it
import operator
import sys
import re

# Fabric
from fabric.api import settings, task, env, run, local, hide
from fabric.colors import red
from fabric.operations import put

# Fabtools
from fabtools import openwrt
from fabtools import require
from fabtools import disk

"""
OpenWrt Parental Control
fab -H root@192.168.253.253 update
fab -H root@192.168.253.253 initfile
fab -H root@192.168.253.253 openfile getdictionary
fab -H root@192.168.253.253 check

fab -H root@192.168.253.253 openfile calcstats filterbycombinations:limit=1000 calcstats:combination showresults showstats bltofile

fab -H root@192.168.253.253 initfile openfile calcstats filterbyexact calcstats:combination showresults showstats
fab -H root@192.168.253.253 initfile openfile calcstats filterbycombinations:nbwords=3 calcstats:combination showresults showstats
"""

debug = True
lines = set()
blacklist = set()
filter_combination = set()
filter_exact = set()
filter_partial = set()
stats = list()

exact_sexwords = set(['ass', 'sex', 'cul', 'sexe', 'tit', 'nude', 'voyeur', 'sexo', 'cocks', 'salope', 'adult', 'tits', 'anal', 'dating', 'cock', 'seins', 'cum'])

partial_sexwords = set(['dicks', 'beurette', 'brunette', 'enlargement', 'bangbus', 'porn', 'pussy', 'fuck', 'sexshop', 'penis', 'erotic', 'sodomie', 'erotik', 'cumshot', 'bite', 'lesbian', 'baise', 'sexcam', 'zoophilie', 'salopes', 'anus', 'gay', 'xxx', 'boobs', 'blowjob', 'webcamsex', 'lesbienne', 'sexy', 'xxn', 'telefonsex', 'bondage', 'gangbang', 'naked', 'livesex'])

combined_sexwords = set([
    'hardcore', 'rencontre', 'free', 'pics', 'teen', 'tumblr', 'startspot', 'girls', 'blog', 'blogspot', 'amateur', 'video', 'picture', 'videos', 'canalblog', 'live', 'teens', 'escort', 'escorts', 'movies', 'movie', 'asian', 'black', 'fetish', 'big', 'cam', 'photo', 'photos', 'gratuit', 'webcam', 'gratis', 'gallery', 'galleries', 'pictures', 'hot', 'online', 'girl', 'babes', 'women', 'amateurs', 'hard', 'cams', 'sessos', 'sesso', 'lingerie', 'mature', 'young', 'ifrance', 'centerblog', 'skyblog', 'femme', 'femmes', 'absentdog','hentai', 'chat', 'site', 'top', 'bdsm', 'shemale', 'cjb', 'best', 'wild', 'lolita', 'stories', 'love', 'geile'
])

ignore_words = set([
    
])



def comp_len(v1, v2):
    if len(v1) < len(v2):
        return -1
    elif len(v1) > len(v2):
        return 1
    else:
        return 0


def comp(v1, v2):
    if v1[0] < v2[0]:
        return -1
    elif v1[0] > v2[0]:
        return 1
    else:
        return 0


@task
def openfile(filename=''):
    global lines
    global blacklist

    if filename == "":
        filename = "/tmp/domains_blacklist"

    with open(filename) as f:
        lines = f.readlines()

    lines = set(lines)
    blacklist = lines


@task
def initfile(filename=''):
    if filename == "":
        filename = "/tmp/blacklist/UT1Blacklist/blacklists/adult/domains"

    local('cp %s /tmp/domains_blacklist' % filename)


@task
def calcstats(name='before'):
    global stats

    s = {}
    s['name'] = name
    s['ramsize'] = sys.getsizeof(blacklist)
    s['nblines'] = len(blacklist)
    stats.append(s)


@task
def check():
    """ Check if the partial sexword not in exact_sexwords"""

    print "E = Exact sexwords / P = partial sexwords / C = combined with sexwords"
    print "----------------------------------------------------------------------"

    # Check if the partial sexwords in exact sexwords
    todelete = set()
    res = exact_sexwords.difference(partial_sexwords)
    for p in partial_sexwords:
        for r in res:
            if p in r:
                todelete.add(r)

    res = res.difference(todelete)
    if res != exact_sexwords:
        print "exact_sexwords = "
        print res
        print ""

    # Check if parten in partial sexwords not conflit
    todelete = set()
    for p in partial_sexwords:
        for pp in partial_sexwords:
            if p in pp and p != pp:
                todelete.add(pp)

    res = partial_sexwords.difference(todelete)
    if res != partial_sexwords:
        print "partial sexwords = "
        print res


@task
def bltofile(filename=''):

    # Write result
    if filename == "":
        filename = "/tmp/domains_blacklist"

    with open(filename, "w") as f:
        for b in blacklist:
            f.write(b)

    #Write filter_combination
    filename = "/tmp/domains_combination"
    with open(filename, "w") as f:
        for combi in filter_combination:
            egrep = ""
            for word in combi:
                egrep += ".*%s" % word

            egrep += "\n"
            f.write(egrep)


@task
def install():
    """
    Install a Parental Control on OpenWrt router
    """

    # Set Shell environment
    env.shell = "/bin/ash -l -c"

    # Install USB required packages
    openwrt.update_index()
    openwrt.install([
        'tinyproxy',
    ])

    print ("Set configuration")

    with settings(hide('running', 'warnings', 'stdout')):
        run('mkdir -p /var/etc/tinyproxy')
        run('echo "youporn" >> /var/etc/tinyproxy/filter')

        run('touch /var/log/tinyproxy.log')
        run('chown nobody:nogroup /var/log/tinyproxy.log')

    openwrt.uci_set([
        "tinyproxy.@tinyproxy[0].Allow=192.168.253.0/24",
        "tinyproxy.@tinyproxy[0].Filter=/var/etc/tinyproxy/filter",
        "tinyproxy.@tinyproxy[0].enabled=1",
        "tinyproxy.@tinyproxy[0].Syslog=0",
    ])

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        run('/etc/init.d/tinyproxy enable')

    update()


@task
def update():
    """
    Update Parental Control with the blacklist UT1
    """

    # Set Shell environment
    env.shell = "/bin/ash -l -c"

    # UT1 Blacklist
    local('mkdir -p /tmp/blacklist/UT1Blacklist')
    local("wget 'ftp://ftp.ut-capitole.fr/pub/reseau/cache/squidguard_contrib/blacklists.tar.gz' -O /tmp/blacklist/UT1Blacklist/blacklists.tar.gz")
    local('tar -xzf /tmp/blacklist/UT1Blacklist/blacklists.tar.gz -C /tmp/blacklist/UT1Blacklist/')

    local('mkdir -p /tmp/blacklist/urlblacklist')
    local("wget 'http://urlblacklist.com/cgi-bin/commercialdownload.pl?type=download&file=bigblacklist' -O /tmp/blacklist/urlblacklist/blacklists.tar.gz")
    local('tar -xzf /tmp/blacklist/urlblacklist/blacklists.tar.gz -C /tmp/blacklist/urlblacklist')
    sys.exit()

    ignores = [
        'ads',
        'drogue',
        'agressif',
    ]

    local('echo "" > /tmp/tinyproxy/filter')
    for ignore in ignores:
        local('cat /tmp/tinyproxy/blacklists/%s/domains >> /tmp/tinyproxy/filter' % ignore)

    put('/tmp/tinyproxy/filter', '/var/etc/tinyproxy/filter')

    with settings(hide('running', 'warnings', 'stdout'), warn_only=True):
        #run('/etc/init.d/tinyproxy stop')
        #run('/etc/init.d/tinyproxy start')
        print(red('Please restart tinyproxy with /etc/init.d/tinyproxy restart'))


def splitedwords(line):
    s = line

    s = re.sub(r'[0-9]+', '', s)
    s = re.sub(r'\-+', ' ', s)
    s = re.sub(r'\.+', '.', s)
    words = s.split(' ')
    return words


@task
def compress(categorie='adult'):

    limit = 3

    # Order ignore by len size ex: sex.com, x.com
    ignoreline.sort(cmp=comp_len, reverse=True)

    for line in lines:
        used = list()
        line = line.replace('\n', '')
        before = line
        tmpline = line

        for i in ignoreline:
            if len(i) > 2 and i in tmpline and i not in used:
                m = re.match(r'.*[0-9]+.*', i)
                if not m:
                    tmpline = tmpline.replace(i, '')
                    used.append(i)
                    if len(used) >= limit:
                        break

        # reorder words
        if len(used) >= limit:
            used = list()
            nbchange = 0
            replace = ""
            words = splitedwords(line)
            for w in words:
                if len(w) > 2 and w in line and w not in used:
                    m = re.match(r'.*[0-9]+.*', w)
                    if not m:
                        used.append(w)
                        replace += ".*%s.*" % w
                        nbchange += 1
                        if nbchange >= limit:
                            break

        if len(used) >= limit:
            # print before
            # print line
            #print "OK: %s/%s" % (replace, before)
            print "OK: %s" % replace
        else:
            print "NO %s" % before


@task
def ignoredomain(categorie='adult'):
    limit = 3

    # Order ignore by len size ex: sex.com, x.com
    ignoreline.sort(cmp=comp_len, reverse=True)
    for line in lines:
        used = list()
        line = line.replace('\n', '')
        before = line
        tmpline = line

        for i in ignoreline:
            if i in tmpline:
                print ("%s/%s" % (i, tmpline))
                sys.exit()

        # reorder words
        if len(used) >= limit:
            used = list()
            nbchange = 0
            replace = ""
            words = splitedwords(line)
            for w in words:
                if len(w) > 2 and w in line and w not in used:
                    m = re.match(r'.*[0-9]+.*', w)
                    if not m:
                        used.append(w)
                        replace += ".*%s.*" % w
                        nbchange += 1
                        if nbchange >= limit:
                            break

        if len(used) >= limit:
            # print before
            # print line
            #print "OK: %s/%s" % (replace, before)
            print "OK: %s" % replace
        else:
            print "NO %s" % before


@task
def getdictionary(limit=1000):
    """Get a top words in domains name"""

    count = {}
    for line in lines:
        words = re.findall('[a-z]{3,}', line)

        for w in words:
            if w in count:
                count[w] += 1
            else:
                count[w] = 1

    topwords = sorted(count.iteritems(), key=operator.itemgetter(1), reverse=True)
    for k, c in topwords[:limit]:
        text = ""
        if k in ignore_words:
            text = "I "

        if k in exact_sexwords:
            text = "E "

        for p in partial_sexwords:
            if p in k:
                text = "P "
                break


        if len(text) == 0:
            text = "  "

        text += "%s=%s" % (k, c)
        print text


def gettopsexcombinations(nbwords=3, limit=100):
    """Get a top words in domains name"""

    badphrases = list()

    for line in lines:
        words = re.findall('[a-z]{3,}', line)

        if len(words) >= nbwords:
            for pair in it.combinations(words, nbwords):
                # pairs[tuple(pair)] += 1
                if len(set(pair)) == nbwords:
                    badphrases.append(pair)
                    # print line
                    # print pair
                    # print set(pair)

    topwords = Counter(badphrases).most_common(limit)
    return topwords

    # print topwords
    # sys.exit()
    # # Search if words exists in other order
    # used = {}
    # for top in topwords:
    #     text = "egrep '"
    #     for p in top[0]:
    #         text += ".*%s.*" % p

    #     text +="'"
    #     print text
    #     sys.exit()

    #     key = tuple(sorted(top[0]))
    #     occurence = top[1]
    #     if key in used:
    #         used[key] += occurence
    #     else:
    #         used[key] = occurence

    # topwords = sorted(used.iteritems(), key=operator.itemgetter(1), reverse=True)

    # return topwords



@task
def filterbycombinations(nbwords=3, limit=100):
    """Search words used in the porn sites"""

    global filter_combination
    global blacklist

    topwords = gettopsexcombinations(int(nbwords), int(limit))

    for combi, c in topwords:
        text = ""
        cexact = 0
        cpartial = 0
        ccombined = 0
        for word in combi:
            if word in exact_sexwords:
                cexact += 1
            if word not in ignore_words:
                ccombined += 1
            for p in partial_sexwords:
                if p in word:
                    cpartial += 1
                    break

        if debug:
            text = ""
            if cexact > 0:
                text += "E%s " % cexact
            else:
                text += "   "

            if cpartial > 0:
                text += "P%s " % cpartial
            else:
                text += "   "

            if ccombined > 0:
                text += "C%s " % ccombined
            else:
                text += "   "

            if ccombined > 0 and (cexact > 0 or cpartial > 0):
                text += "[X]"
            else:
                text += "[_]"

            text += "%s = %s" % (combi, c)
            print text
        else:
            if ccombined > 0 and (cexact > 0 or cpartial > 0):
                    for word in combi:
                        filter_combination.add(combi)



    lwords = len(filter_combination)
    pos = 0;
    result = set()
    egrep = ""
    for combi in filter_combination:
        pos += 1
        print "Pos (%s/%s) / %s)" % (pos, lwords, combi)
        egrep += ""
        for word in combi:
            egrep += ".*%s" % word

        egrep += "|"

    egrep += "^$"
    for l in lines:
        m = re.match(egrep, l)
        if m:
            result.add(l)

    blacklist = blacklist.difference(result)


@task
def showresults():
    print filter_combination

@task
def showstats():
    print "Memory stats"
    print "------------"

    #bramsize = stats[0]['ramsize'] / 1024 / 1024
    bnblines = stats[0]['nblines']
    for s in stats:
        #ramsize = s['ramsize'] / 1024 / 1024
        nblines = s['nblines']
        #dramsize = bramsize - ramsize
        dnblines = bnblines - nblines
        ratio = round((dnblines / float(bnblines) * 100),2)
        #print "%s RAMSIZE = %s Mo / gain de %s Mo" % (s['name'], ramsize, dramsize)
        print "%s NBLINES = %s / gain de (%s%%) %s lignes" % (s['name'], nblines, ratio, dnblines)

# # VALIDE
# @task
# def searchsexcombinations(filename='', searchstart=3, searchend=2, limit=1000):
#     """Search words used in the porn sites"""

#     global sexwords

#     usedinpornsites = getsexwords4pornsites(
#         filename,
#         searchstart,
#         searchend,
#         limit
#     )

#     for k, t in usedinpornsites:
#         sexwords.add(k)

#     res = "sexwords = {\n    "
#     lensize = 0
#     for k in sexwords:
#         tmp = "'%s'" % k
#         res += tmp
#         lensize += len(tmp) + 2
#         if lensize > 60:
#             lensize = 0
#             res += ",\n    "
#         else:
#             res += ", "

#     res += "\n}"
#     print res


def getfilters(filename='', nbwords=3, limit=100):

    topwords = gettopsexwordscombinations(filename, nbwords)

    egrep = ""
    used = {}
    for top in topwords:

        key = tuple(sorted(top[0]))
        occurence = top[1]
        if key in used:
            used[key] += occurence
        else:
            used[key] = occurence

        for nbcombi in it.permutations(top[0], nbwords):
            egrep += "("
            for w in nbcombi:
                egrep += "%s.*" % w

            egrep += ")|"
        #egrep += "^$'"
        egrep +="^$\n"
    #print egrep

    filters = sorted(used.iteritems(), key=operator.itemgetter(1), reverse=True)

    return filters


@task
def filters(filename='', nbwords=3, limit=100):

    global lines

    datas = getfilters(filename, nbwords, limit)

    result = set()
    for d in datas:
        egrep = ""
        #print "calc for %s" % repr(d[0])
        for nbcombi in it.permutations(d[0], nbwords):
            egrep += "("
            for w in nbcombi:
                egrep += "%s.*" % w

            egrep += ")|"

        egrep += "^$"

        for l in lines:
            m = re.match(egrep, l)
            if m:
                result.add(l)

    diff = lines.difference(result)

    # print len(lines)
    # print len(result)
    # print len(diff)
    print (diff)
    sys.exit()
    print datas


@task
def filterbyexacts():

    global blacklist

    result = set()
    for d in exact_sexwords:
        egrep = ".*[\.\-]%s[\.\-].*" % d

        for l in lines:
            m = re.match(egrep, l)
            if m:
                result.add(l)

    blacklist = blacklist.difference(result)


@task
def filterbypartial():

    global blacklist

    result = set()
    for d in partial_sexwords:
        egrep = ".*%s.*" % d

        for l in lines:
            m = re.match(egrep, l)
            if m:
                result.add(l)

    blacklist = blacklist.difference(result)

# @task
# def bl_domains(categorie='adult', limit=1000):

#     words = getdictionary(categorie)

#     domains = list()
#     for w in words[:limit]:
#         m = re.match(r'[a-z]+\.[a-z]{2,5}$', w[1])
#         if m:
#             domains.append(w[1])

#     #domains.sort(cmp=comp_len, reverse=True)
#     res = "ignoreline = ["
#     for c in domains[:limit]:
#         res += "'%s', " % c
#     res += "]"

#     print res

@task
def searchdomain(categorie='adult', limit=100):

    words = getdictionary(categorie)

    r = "cat domains| egrep '"
    for (c, w) in words[:limit]:
        r += "[\.\-]%s[\.\-]|" % w
    r += "^$'"
    print r
    sys.exit()

    ignore = {}
    count = {}
    for line in lines:
        line = line.replace('\n', '')

        m = re.match(r'([0-9\.\-]+)(\.[a-z\.\-]+)', line)
        if m:
            r = m.group(2)
            if r not in ignore:
                if r in count:
                    count[r] += 1
                else:
                    count[r] = 1

    countorder = list()
    for word, times in count.items():
        countorder.append([times, word])

    countorder.sort(cmp=comp, reverse=True)

    for w in countorder[:100]:
        print w
    sys.exit()


    # countorder.sort(cmp=comp, reverse=True)
    # return countorder


@task
def getdomains(categorie='adult'):

    words = getdictionary(categorie)

    res = list()
    for w in words[:1000]:
        m = re.match(r'[a-z]+\.[a-z]{2,5}$', w[1])
        if m:
            res.append(w[1])

    res.sort(cmp=comp_len, reverse=True)
    print res

    # res = "ignoreline = ["
    # for c in countorder[:1000]:
    #     res += "'%s', " % c[1]
    # res += "]"

    # print res
