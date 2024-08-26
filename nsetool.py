from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import random
from datetime import datetime, timedelta
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
from kline_pre import kline_pre

# 代码列表
def get_stock_codes():
    return [
            'INFY', 'TCS', 'RELIANCE', 'HDFCBANK', 'ITC', 'KOTAKBANK', 'SBIN', 'HINDUNILVR', 'ICICIBANK', 'BAJFINANCE',
        'ADANIPORTS', 'ASIANPAINT', 'AUROPHARMA', 'AXISBANK', 'BAJAJ-AUTO', 'BAJAJFINSV', 'BAJAJHLDNG', 'BPCL',
        'BHARTIARTL', 'INFRATEL', 'COALINDIA', 'DRREDDY', 'EICHERMOT', 'GAIL', 'GRASIM', 'HCLTECH', 'HDFC',
        'HEROMOTOCO', 'HINDALCO', 'HINDZINC', 'JSWSTEEL', 'M&M', 'MARUTI', 'NESTLEIND', 'NTPC', 'ONGC',
        'POWERGRID', 'SHREECEM', 'SUNPHARMA', 'TATAMOTORS', 'TATASTEEL', 'TECHM', 'ULTRACEMCO', 'UPL', 'VEDL',
        'WIPRO', 'ZEEL', 'YESBANK', 'BOSCHLTD', 'CIPLA', 'DIVISLAB', 'GODREJCP', 'HAVELLS', 'HDFCLIFE', 'ICICIPRULI',
        'IGL', 'INDIGO', 'INDUSINDBK', 'NAUKRI', 'PIDILITIND', 'SRF', 'TORNTPHARM', 'MCDOWELL-N', 'UBL', 'AMBUJACEM',
        'APOLLOHOSP', 'AUROPHARMA', 'BANKBARODA', 'BERGEPAINT', 'BIOCON', 'CADILAHC', 'CANBK', 'COLPAL', 'DABUR',
        'DLF', 'ESCORTS', 'EXIDEIND', 'GLENMARK', 'GMRINFRA', 'GODREJPROP', 'IDEA', 'INDHOTEL', 'JINDALSTEL', 'L&TFH',
        'LICHSGFIN', 'MOTHERSUMI', 'PEL', 'PFIZER', 'PGHH', 'PNB', 'RECLTD', 'SAIL', 'SIEMENS', 'SRTRANSFIN',
        'TATACONSUM', 'TATAPOWER', 'TVSMOTOR', 'UNIONBANK', 'VOLTAS', 'WHIRLPOOL', 'ADANIGREEN', 'ADANITRANS',
        'BAJAJHLDNG', 'BANDHANBNK', 'BHEL', 'CHOLAFIN', 'COFORGE', 'DMART', 'GODREJAGRO', 'HONAUT', 'IOC', 'IRCTC',
        'LTTS', 'LUPIN', 'MFSL', 'MPHASIS', 'MUTHOOTFIN', 'NAM-INDIA', 'PETRONET', 'PFC', 'RAMCOCEM', 'SBILIFE',
        'TATACHEM', 'TRENT', 'ADANIENT', 'ATGL', 'CROMPTON', 'DEEPAKNTR', 'GUJGASLTD', 'HINDPETRO', 'IIFLWAM',
        'LINDEINDIA', 'METROPOLIS', 'PAGEIND', 'PERSISTENT', 'RBLBANK', 'SUNDARMFIN', 'SUPREMEIND', 'ABB', 'ABFRL',
        'ACC', 'AIAENG', 'AJANTPHARM', 'ALEMBICLTD', 'ALKEM', 'ALLCARGO', 'AMARAJABAT', 'AMBER', 'APARINDS',
        'APLAPOLLO', 'APLLTD', 'AARTIIND', 'AUBANK', 'AVANTIFEED', 'BALKRISIND', 'BALRAMCHIN', 'BBTC', 'BEL',
        'BEML', 'BFINVEST', 'BLUEDART', 'BRIGADE', 'CANFINHOME', 'CESC', 'CHAMBLFERT', 'CHOLAINV', 'CONCOR',
        'COROMANDEL', 'CUB', 'CYIENT', 'DCBBANK', 'DCMSHRIRAM', 'DELTACORP', 'DISHTV', 'DIXON', 'EIDPARRY',
        'ENDURANCE', 'FDC', 'FRETAIL', 'GDL', 'GMMPFAUDLR', 'GPPL', 'GSFC', 'GSPL', 'HATSUN', 'HEG', 'HFCL',
        'HGS', 'HIKAL', 'HSCL', 'HUDCO', 'IBULHSGFIN', 'IDFC', 'IDFCFIRSTB', 'IEX', 'IFCI', 'IGARASHI', 'INDIANB',
        'INDOCO', 'INDRAMEDCO', 'IOLCP', 'IPCALAB', 'IRB', 'ISEC', 'ITDC', 'ITDCEM', 'JBCHEPHARM', 'JCHAC',
        'JINDALSAW', 'JKCEMENT', 'JKLAKSHMI', 'JMFINANCIL', 'JSL', 'JSLHISAR', 'JSWENERGY', 'JUBLPHARMA',
        'JUBLFOOD', 'JYOTHYLAB', 'KALPATPOWR', 'KARURVYSYA', 'KEC', 'KNRCON', 'KSB', 'LAOPALA', 'LAXMIMACH',
        'LEMONTREE', 'LINCOLN', 'MAHABANK', 'MAHINDCIE', 'MAHLOG', 'MANAPPURAM', 'MAYURUNIQ', 'MBLINFRA', 'MCX',
        'MEGH', 'MFSL', 'MGL', 'MINDTREE', 'MMTC', 'MOIL', 'MOTILALOFS', 'MRPL', 'MUTHOOTFIN', 'NBCC', 'NAVINFLUOR',
        'NBVENTURES', 'NESCO', 'NLCINDIA', 'NMDC', 'NOCIL', 'NTPC', 'OLECTRA', 'OMAXE', 'ONELIFECAP', 'ORIENTELEC',
        'ORIENTREF', 'PAPERPROD', 'PGEL', 'PHOENIXLTD', 'PIDILITIND', 'POLYPLEX', 'PRAJIND', 'PRINCEPIPE',
        'PSPPROJECT', 'PTC', 'PVR', 'RADICO', 'RAIN', 'RAJESHEXPO', 'RALLIS', 'RATNAMANI', 'RAYMOND', 'REDINGTON',
        'RELAXO', 'RELINFRA', 'REPCOHOME', 'RITES', 'RVNL', 'SANOFI', 'SAREGAMA', 'SCI', 'SEQUENT', 'SHARDACROP',
        'SHILPAMED', 'SHOPERSTOP', 'SHRIRAMCIT', 'SIEMENS', 'SIS', 'SJVN', 'SKFINDIA', 'SOBHA', 'SOLARINDS',
        'SOUTHBANK', 'SPANDANA', 'SPICEJET', 'SRF', 'STARCEMENT', 'STLTECH', 'SUBROS', 'SUNCLAYLTD', 'SUNTV',
        'SUPPETRO', 'SUVENPHAR', 'SWSOLAR', 'SYNGENE', 'TATAMTRDVR', 'TATAPOWER', 'TCI', 'TCNSBRANDS', 'TEAMLEASE',
        'TECHM', 'THERMAX', 'TIINDIA', 'TINPLATE', 'TITAN', 'TML', 'TRENT', 'TRIDENT', 'TRITURBINE', 'TUBEINVEST',
        'TVTODAY', 'UBL', 'UCOBANK', 'UJJIVAN', 'ULTRACEMCO', 'UNICHEMLAB', 'UPL', 'VAIBHAVGBL', 'VBL', 'VGUARD',
        'VINATIORGA', 'VOLTAMP', 'VSTIND', 'WABCOINDIA', 'WELCORP', 'WELSPUNIND', 'WESTLIFE', 'WIPRO', 'WOCKPHARMA',
        'YESBANK', 'ZEEL', 'MTARTECH', 'LATENTB', 'CARTRADE', 'VYOME', 'UTIAMC', 'STAR', 'ADITYA', 'SFB', 'RANGE',
        'TFCILTD', 'CGCL', 'VYASGLASS', 'SUN', 'ASL', 'WHISPER', 'BLUECHIP', 'CAMCONC', 'RUMA', 'CCCL', 'NATIONSTD',
        'CENTRUM', 'HIND', 'BLUECOAST', 'EARTH', 'STURDY', 'AMB', 'VARIABLE', 'INDIUM', 'KEMCORP', 'SRIRAM',
        'RASI', 'PAP', 'PURVA', 'DION', 'NIRMITEE', 'SHYAMSAL', 'AHA', 'KVSTEX', 'AMIDHARA', 'ELDER', 'BHAGYANGR',
        'MANG', 'GMFL', 'SUKRITI', 'RADIO', 'MURABLUE', 'GUJRAFFIA', 'SALGAVIS', 'ABSLBANETF', 'JMCGLOBAL',
        'SFL', 'KNR', 'ZUARI', 'GEPL', 'KSOL', 'GCMSECU', 'HDFCAMC', 'EASTSILK', 'WALCHANNAG', 'PRINCE', 'BHARATRAS',
        'AMMANN', 'SUPRAJIT', 'SAKAR', 'CUPID', 'TATACAP', 'NBCC', 'NATHBIOGEN', 'EASY', 'KREBSBIO', 'IMFA',
        'NITINSPIN', 'CPSEETF', 'KARDA', 'RAJAS', 'PRIME', 'ZESTFIN', 'INNOVANA', 'COSBOARD', 'MATRIMONY', 'HATHWAY',
        'SIRCA', 'SHREYANIND', 'EBI', 'GAYAHWS', 'PIRAMAL', 'LSIL', 'MULTI', 'FSL', 'NAVKAR', 'VRWOOD', 'TEAM',
        'JAGSONPAL', 'PATDYES', 'ATLANTA', 'CANOPY', 'UHPL', 'MEERA', 'QUINTEGRA', 'MBECL', 'LADLOI', 'KOVAI',
        'IOLCHEM', 'MIDHANI', 'SUMICHEM', 'HIL', 'MMFSL', 'KIRIINDUS', 'MIDHANI', 'HIL', 'MMFSL', 'KIRIINDUS',
        'HIL', 'KIRIINDUS', 'MIDHANI', 'UNIVASTU', 'TAPOVAN', 'ARTEFACT', 'RCL', 'ENSO', 'ARENERGY', 'MIRZAINT',
        'BHEL', 'KRBL', 'KOSAMATTAM', 'DECCANCE', 'SHARIKA', 'MOKSH', 'KSHITIJ', 'RRPL', 'AWHCL', 'POLYPLEX',
        'SRIPIPES', 'GULFOILLUB', 'SAHAKAAR', 'INTELLECT', 'AGROPHOS', 'MARISPA', 'AGRITECH', 'POWERFUL', 'SANDHYA',
        'MELSTAR', 'SUYOG', 'ASHARI', 'MSK', 'PRESTIGE', 'OMAXAUTO', 'BRIJDYE', 'SURANAT', 'SARVESH', 'MSRIND',
        'DALALSTRE', 'KRATOS', 'SHIVAEXPO', 'RRIL', 'NEOGEN', 'ACCORD', 'NIFTY', 'KAYCEE', 'PANTH', 'MURUDCERA',
        'MOTOGENFIN', 'MIRZA', 'ZUARIGLOB', 'ALANKIT', 'CANTABIL', 'GLOBUSSPR', 'GCMSEC', 'SUVEN', 'COUNCODOS',
        'KSERASERA', 'BLS', 'GENNEX', 'BARBEQUE', 'PIONDIST', 'SUVEN', 'PRINCEPIPE', 'EPL', 'SAR', 'AXITA',
        'UNIPLY', 'EMAMI', 'GOLCAPTA', 'INDBANK', 'CHANDRAP', 'CPML', 'ADVIK', 'LAXMIMACH', 'PARRYSUG', 'TRITURBINE',
        'BGIL', 'OMAXE', 'WELSPUN', 'PRABHAT', 'KHAICHEM', 'KARURVYSYA', 'TECHIND', 'VEEJAY', 'NIDECO', 'BEARDSELL',
        'MEGASOFT', 'DOLLAR', 'BLISSGVS', 'MOTHERSUMI', 'ORBITEX', 'JAGSNPHARM', 'SUJANAUNI', 'BANNARI', 'RCAP',
        'AGCNET', 'GKB', 'GIPCL', 'RUSHIL', 'GALAXYSURF', 'VAMA', 'ADCL', 'SUNDARAM', 'MANUGRAPH', 'ERIS',
        'GODHA', 'LICNETFN50', 'VANDANA', 'NIBE', 'SHAKTIPUMP', 'SHAKTIPUMP', 'ANDHRSUGAR', 'SPIC', 'TECHNOFAB',
        'SUNTECK', 'NAHARINDU', 'GAYAPROJ', 'REVATHI', 'TATASTEEL', 'MUKANDENGG', 'CUBEXTUB', 'PNCINFRA',
        'LAKPRE', 'NATNLSTEEL', 'WINSOME', 'NATIONALUM', 'SHIVAMAUT', 'VSSL', 'GANGOTRI', 'MURLIIND', 'CALSOFT',
        'HINDZINC', 'HINDDORR', 'REXNORD', 'CTE', 'COMSYN', 'INFRABEES', 'SIEMTRX65', 'AMBACFIN', 'KCP', 'THEMISMED',
        'BANCOINDIA', 'HINDMOTORS', 'VISAKAIND', 'A2ZINFRA', 'TANLA', 'AARTIDRUGS', 'SUNDARAM', 'JSWHL', 'SURANA',
        'PSL', 'BRFL', 'MORARJEE', 'CUBEXTUB', 'HINDMOTORS', 'PRAENG', 'SHRIRAMEPC', 'GRAUWEIL', 'NAGREEKCAP',
        'WINDSOR', 'TRF', 'RAMGOPOLY', 'ROHITFERRO', 'METROPO', 'DEEPENER', 'XPROINDIA', 'WENDT', 'ALPHAGEO',
        'SIMPLEX', 'AVONMORE', 'MEGASOFT', 'CTE', 'MINDTECK', 'RUCHINFRA', 'RAJRAYON', 'KEWIND', 'CLNINDIA',
        'NRAIL', 'NEPCAGRO', 'MRO-TEK', 'UNITECH', 'TRIVENIGQ', 'CHOKHANI', 'ADROITINFO', 'MARGOFIN', 'WEBELSOLAR',
        'SUVEN', 'MAXIMAA', 'IMPEXFERRO', 'ICIL', 'GSLNOVA', 'INDRAMEDCO', 'MSPL', 'RICOAUTO', 'IFGLREFRAC',
        'MODIRUBBER', 'JAYNECOIND', 'JIKIND', 'SPMLINFRA', 'BGRENERGY', 'SOLIT', 'SAKSOFT', 'EUROTEXIND',
        'GANESHHOUC', 'SWASTIKIND', 'ARIHANT', 'TANVI', 'REIAGROLTD', 'JAYBHCR', 'VICTORY', 'RIGASUGAR', 'KKVAPOW',
        'BAJAJFINSV', 'AMJLAND', 'CIGNITITEC', 'GOKUL', 'VARROC', 'KEERTI', 'INDAG', 'VIJSHAN', 'PIONEEER',
        'BODALCHEM', 'VINDHYATEL', 'UVSL', 'ELGIRUBCO', 'NITIN', 'USGTECH', 'IFBIND', 'GSHPROP', 'KICL',
        'GANDHITUBE', 'AFL', 'GENUSPAPER', 'AJMERA', 'DHP', 'SIMBHALS', 'VIVIMEDLAB', 'GPIL', 'SPIC', 'GOACARBON',
        'SPECTACLE', 'RUBYMILLS', 'JAYNECOIND', 'JKPAPER', 'SANWARIA', 'PHILIPCARB', 'NORBTEAEXP', 'SAMBHAAV',
        'JAYAGROGN', 'SIEMTRX65', 'SATIA', 'DISHMAN', 'JPINFRATEC', 'SOFTTEKIND', 'AARTISURF', 'PERSISTENT',
        'FILATEX', 'HERITGFOOD', 'BANG', 'VALIANTORG', 'UFO', 'STERLINBIO', 'VGUARD', 'NECLIFE', 'AMBALALSA',
        'GOENKA', 'BCG', 'WEIZFOREX', 'MMWL', 'KAKATCEM', 'JAYBHAGAT', 'AVTNPL', 'BAFNAPH', 'STARLIM', 'SSWL',
        'EON', 'PHTRADING', 'PGIL', 'MONTECARLO', 'BAGFILMS', 'RATHIB', 'WEBSL', 'RISHIRAV', 'BSL', 'PRAKASH',
        'PITHAMPUR', 'GOLDIWIN', 'CANFIHOM', 'COMFORTIN', 'MOTILALOFS', 'SUNRAJDI', 'SUPREMEINF', 'CSBBANK',
        'SHILPAMED', 'ORICONENT', 'MUKANDENGG', 'EONBONDS', 'PIG", "PANACHE", "NESCOBPO", "POLARIND',
        'RADICO', 'YAMUNAFOOD', 'KABRAEXTRU', 'SAWACA', 'ADVANIHOT', 'DBREALTY', 'AISWARYA', 'ANUP', 'MOUNT',
        'DIAPOWER', 'NRB', 'JAYATMA', 'SHARDACROP', 'JIKIND', 'SHIVALIK', 'TWILIT', 'GEMINIPRINT', 'CRAVATEX',
        'THYROCARE', 'BLS', 'AMTINTL', 'GRAPHITE', 'ADMANUM', 'UNITEDTEA', 'MSPL', 'SADBHIN', 'TRANSWIND',
        'EVERESTIND', 'CHROMATIC', 'PGCIL', 'VENKYS', 'OMINFRAL', 'PAISALO', 'RAMASTEEL', 'SANGHVIMOV', 'FOCUS',
        'WIMPLAST', 'MUKTAARTS', 'ELECON', 'KARDA', 'EASTSILK', 'BANCOINDIA', 'MUNAKISHO', 'UJJIVAN', 'MAYUR',
        'ORICONENT', 'CLEDUCATE', 'SABOO', 'NATPEROX', 'NECCORP', 'MEGASTAR', 'NINL', 'SSWL', 'TMRVL', 'ASIL',
        'ORIENTABRA', 'FELIX', 'SHREEASHT', 'MORGANITE', 'RUCHIRA', 'SIMRAN', 'CYBERMEDIA', 'ADVANIHOT', 'VICEROY',
        'VINDHYATL', 'SAKSOFT', 'PARRYSUG', 'ZYDUSWELL', 'PTCIND', 'RIDDHI', 'SUPRAJIT', 'LINCOLN', 'NDA',
        'MANINFRA', 'MSPL', 'TNPL', 'UNITECH', 'SUNTV', 'BHAGWATI', 'GSS', 'KMSUGAR', 'BIOFILCHEM', 'NCLRESE',
        'SUMEETIND', 'RAMCOIND', 'STER', 'UNITECH', 'BANKBEES', 'VISAKAIND', 'VSTTILLERS', 'ZICOM', 'UBHOLDINGS',
        'PLASTIBLEN', 'KAVVERITEL', 'PRECISION', 'MEGH', 'GESHIP', 'GBGLOBAL', 'PENINLAND', 'MAANALU', 'THAKRAL',
        'CIGNITITEC','SANSTAR','DECCAN','POBS'
    ]


def get_stock_info(page, per_page=10, sort_by=None, query_code=None):
    stock_codes = get_stock_codes()
    if query_code and query_code not in stock_codes:
        stock_codes.append(query_code)
    random.shuffle(stock_codes)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_codes = stock_codes[start:end]

    stock_info_array = []
    for code in paginated_codes:
        try:
            ticker = f"{code}.NS"
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                last_quote = hist.iloc[-1]
                math_value = last_quote['Close']
                prasent = (last_quote['Close'] - last_quote['Open']) / last_quote['Open'] * 100
                formatted_info = {
                    'label': code,
                    'placeholder': stock.info.get('longName', 'N/A'),
                    'mathValue': math_value,
                    'prasent': f"{prasent:.2f}%"
                }
                stock_info_array.append(formatted_info)
            else:
                print(f"No data for {code}")
        except Exception as e:
            print(f"Error fetching data for {code}: {e}")

    if sort_by == 'price':
        stock_info_array.sort(key=lambda x: x['mathValue'], reverse=True)
    elif sort_by == 'growth':
        stock_info_array.sort(key=lambda x: float(x['prasent'].strip('%')), reverse=True)

    return stock_info_array


@app.route('/stocks', methods=['GET'])
def stocks():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        sort_by = request.args.get('sort_by', None)
        query_code = request.args.get('query_code', None)

        if sort_by == 'price':
            stock_info_array = get_stock_info(page, per_page, sort_by='price', query_code=query_code)
        elif sort_by == 'growth':
            stock_info_array = get_stock_info(page, per_page, sort_by='growth', query_code=query_code)
        else:
            stock_info_array = get_stock_info(page, per_page, query_code=query_code)

        return jsonify(stock_info_array)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/trend', methods=['GET'])
def stock_trend():
    stock_code = request.args.get('stock_code', default=None)
    if stock_code:
        return jsonify(get_stock_trend(stock_code))
    else:
        return jsonify({'error': 'Stock code is required.'}), 400


@app.route('/kline', methods=['GET'])
def kline():
    stock_code = request.args.get('stock_code')
    try:
        period = request.args.get('period', '1mo')
        if stock_code:
            response = get_kline_data(stock_code, period)
            if "error" in str(response):
                return kline_pre(stock_code)
            else:
                return jsonify(response)
        else:
            return kline_pre(stock_code)
    except:
        return kline_pre(stock_code)



def get_stock_trend(stock_code):
    ticker = f"{stock_code}.NS"
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    if not hist.empty:
        close_prices = hist['Close'].tolist()
        first_close = hist['Close'].iloc[0]
        last_close = hist['Close'].iloc[-1]
        percent_change = ((last_close - first_close) / first_close) * 100

        last_day = hist.iloc[-1]
        current_price = last_day['Close']
        prasent = (last_day['Close'] - last_day['Open']) / last_day['Open'] * 100
        prasent_str = f"{prasent:.2f}" if prasent < 0 else f"+{prasent:.2f}"

        return {
            'stock': stock_code,
            'close_prices': close_prices,
            'percent_change': percent_change,
            'current_price': current_price,
            'prasent': prasent_str
        }
    else:
        return {'error': 'No data available for the specified stock code.'}


def get_kline_data(stock_code, period='1mo'):
    if '(' in stock_code:
        stock_code = stock_code.split('(')[0].strip()

    ticker = f"{stock_code}.NS" if not stock_code.endswith('.NS') else stock_code
    stock = yf.Ticker(ticker)
    try:
        hist = stock.history(period=period)
        if not hist.empty:
            return {
                'stock': stock_code,
                'period': period,
                'categories': hist.index.strftime('%Y/%m/%d').tolist(),
                'series': [{
                    'name': 'Kline',
                    'data': hist[['Open', 'Close', 'Low', 'High']].values.tolist()
                }]
            }
        else:
            return {'error': f'No data available for {stock_code} with period {period}.'}
    except Exception as e:
        return {'error': str(e)}


@app.route('/search_stocks', methods=['GET'])
def search_stocks():
    query = request.args.get('query', default="")
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    stock_codes = get_stock_codes()
    filtered_stocks = [stock for stock in stock_codes if query.lower() in stock.lower()]

    start = (page - 1) * per_page
    end = start + per_page
    paginated_stocks = filtered_stocks[start:end]

    stock_info_array = []
    for code in paginated_stocks:
        try:
            ticker = f"{code}.NS"
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                last_quote = hist.iloc[-1]
                formatted_info = {
                    'label': f"{code}(nse)",
                    'placeholder': stock.info['longName'],
                    'mathValue': last_quote['Close'],
                    'prasent': f"{(last_quote['Close'] - last_quote['Open']) / last_quote['Open'] * 100:.2f}%"
                }
                stock_info_array.append(formatted_info)
            else:
                print(f"No data for {code}")
        except Exception as e:
            print(f"Error fetching data for {code}: {e}")

    return jsonify(stock_info_array)


def fetch_stock_info(stock_code):
    ticker = f"{stock_code}.NS"
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1d")
    if not hist.empty:
        last_quote = hist.iloc[-1]
        math_value = last_quote['Close']
        prasent = (last_quote['Close'] - last_quote['Open']) / last_quote['Open'] * 100
        return {
            'label': stock_code,
            'placeholder': stock.info.get('longName', 'N/A'),
            'mathValue': math_value,
            'prasent': f"{prasent:.2f}%"
        }
    else:
        return {'error': f"No data for {stock_code}"}
    




@app.route('/check_stock', methods=['GET'])
def check_stock():
    stock_code = request.args.get('stock_code')
    data_type = request.args.get('data_type', 'stock')  # 'stock' or 'kline'
    period = request.args.get('period', '1mo')
    
    if not stock_code:
        return jsonify({'error': 'Stock code is required.'}), 400

    stock_codes = get_stock_codes()
    
    response = {'status': 'not_found'}

    if stock_code in stock_codes:
        response['status'] = 'exists'

    if data_type == 'stock':
        stock_info = fetch_stock_info(stock_code)
        response['data'] = stock_info
    elif data_type == 'kline':
        kline_data = get_kline_data(stock_code, period)
        response['data'] = kline_data
    else:
        return jsonify({'error': 'Invalid data type. Choose either "stock" or "kline".'}), 400
    
    return jsonify(response)



# 获取所有数据
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1mo")
        
        if data.empty:
            return {"error": f"No data available for ticker: {ticker}"}
        
        close_prices = data['Close'].tolist()
        current_price = data['Close'].iloc[-1]
        percent_change = ((close_prices[-1] - close_prices[0]) / close_prices[0]) * 100
        return {
            "close_prices": close_prices,
            "current_price": current_price,
            "percent_change": round(percent_change, 2),
            "prasent": f"{round(percent_change, 2)}%",
            "stock": ticker
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/get_sensex_data', methods=['GET'])
def get_sensex_data():
    ticker = '^BSESN'
    stock_data = fetch_stock_data(ticker)
    return jsonify(stock_data)

@app.route('/get_nifty50_data', methods=['GET'])
def get_nifty50_data():
    ticker = '^NSEI'
    stock_data = fetch_stock_data(ticker)
    return jsonify(stock_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5588, debug=True)
