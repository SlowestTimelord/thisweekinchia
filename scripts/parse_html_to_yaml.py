from bs4 import BeautifulSoup
import re
import yaml

html = """
<h3>Week of August 20, 2023 - August 26, 2023 <div class="week"><span class="tooltip"><a href="https://dexie.space/offers/col1sde4nh5e8xj6l9qjqemu0npel3jnpulqx3xvlcmafjwz5srlgdeqn8tak4/xch" target="_blank"></a><fieldset><a href="https://dexie.space/offers/col1sde4nh5e8xj6l9qjqemu0npel3jnpulqx3xvlcmafjwz5srlgdeqn8tak4/xch" target="_blank"><img width="300px" src="ads/20230820.png" alt="Chia Music" title="Chia Music"></a><legend></legend></fieldset></span></div></h3>
<ul>
	<li class="weekday">TUESDAY • 08/22/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/tjumpx" target="_blank">@tjumpx</a> annouces "XCHscan 2.0 will have a nice UI for this. Although if anyone wants the actual TxStreet visualization for Chia, they recently started open sourcing their code..." <a href="https://twitter.com/tjumpx/status/1694136155854229644?s=20" target="_blank">Source</a> • <a href="https://github.com/txstreet/txstreet" target="_blank">txstreet</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/acevail_" target="_blank">@acevail_</a> announces xch.events, a real time feed of all event happening on the #Chia blockchain! It smartly groups coins together into transactions, based on parent-child and announcements. Future features will be better visualization, offer grouping and een more puzzle parsers. The real time feed will be available for all Chia developers to use! <a href="https://twitter.com/acevail_/status/1694057598989828528?s=20" target="_blank">Source</a> • <a href="https://xch.events/" target="_blank">xch.events</a></li>
	<hr class="daydivide">
	<li class="weekday">MONDAY • 08/21/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/VoskCoin" target="_blank">@VoskCoin</a> releases new video "My Shed for Hard Drive Mining is HERE!" <a href="https://twitter.com/VoskCoin/status/1693693646258811011?s=20" target="_blank">Source</a> • <a href="https://www.youtube.com/watch?v=_3VqHTmoSCw" target="_blank">Watch</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/youtube.png"> <a href="https://twitter.com/monkeyzoo" target="_blank">@monkeyzoo</a> releases several new videos: <a href="https://www.youtube.com/@monkeyzoo6698/videos" target="_blank">Monkeyzoo YouTube</a><br>
		<blockquote class="event_block">
			- How to create a Chia blockchain desktop wallet. Version TWO • <a href="https://www.youtube.com/watch?v=GC8R6kzr2aE" target="_blank">Watch</a><br>
			- How to buy an NFT on the Chia Blockchain • <a href="https://www.youtube.com/watch?v=YXw20kzZ_ME" target="_blank">Watch</a><br>
			- How to Enable Chia Asset Tokens CATs • <a href="https://www.youtube.com/watch?v=eYHknflVTEA" target="_blank">Watch</a><br>
			- How to sell an NFT of the Chia blockchain • <a href="https://www.youtube.com/watch?v=-Ewxy_lr2SA" target="_blank">Watch</a><br>
			- How to create a Chia D I D Decentralised identification • <a href="https://www.youtube.com/watch?v=VjYAaeP91d8" target="_blank">Watch</a><br>
			- Chia Clawbacks • <a href="https://www.youtube.com/watch?v=2Ibzu6RZ3EU&amp;t=313s" target="_blank">Watch</a>
		</blockquote>
	</li>
	<hr class="daydivide">
	<li class="weekday">SUNDAY • 08/20/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/ChiChiverse_NFT" target="_blank">@ChiChiverse_NFT</a> teases a return of ChiChi... Soon™. <a href="https://twitter.com/ChiChiverse_NFT/status/1693427213734203506?s=20" target="_blank">Source</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/bramcohen" target="_blank">@bramcohen</a> announces he is stepping away from X (formerly Twitter) for a while and will be writing on Substack. <a href="https://twitter.com/bramcohen/status/1693336516561699290?s=20" target="_blank">Source</a> • <a href="https://bramcohen.com/" target="_blank">Bram's Thoughts</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/SlowestTimelord" target="_blank">@SlowestTimelord</a> announced a new stablecoin CAT called 🥔 POTATO that is supposedly pegged to $0. <a href="https://twitter.com/SlowestTimelord/status/1693286972788261305" target="_blank">Source</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/spaces.png"> <span style="color:#8C52FE">Twitter Space</span> - Hosted by <a href="https://twitter.com/monkeyzoo" target="_blank">@monkeyzoo</a> "🌱Chia Royalties Guaranteed🌱 Finance &amp; NFT Royalty chat #Chiafixedit" on Sunday August 20, 2023 at 6:00 PM UTC. <a href="https://twitter.com/monkeyzoo/status/1693271888875700649?s=20" target="_blank">Join</a></li>
	<hr class="daydivide">
</ul>

<blockquote>
	<a href="https://www.xchcentral.com/"><img class="weeklyhighlightbanner" src="assets/images/XCHcentral.png"></a>
	<span style="color:#8C52FE">Weekly Highlight:</span> <span style="color:#00AA33">XCHCentral</span>! A well deserving core community member providing a valuable service to everyone with insightful, informative articles &amp; one of the most collectible NFT collections in Chia (Hi ChiChi 👋). Join me in showing some love if you want: <span style="color:#00CC11">xch1dwm59nranz0khzfzmv0j9g4tpwe4fx7ven0ptr9hufs2c0kgesxq8r7mws</span> or see their <a href="https://www.xchcentral.com/" target="_blank">site</a>. <span style="color:#00AA33">💗</span>
	<!-- <br><br> -->
	<img class="weeklyhighlight" src="https://thisweekinchia.com/donations/20230820.png">
</blockquote>
					
<hr>
	

<h3>Week of August 13, 2023 - August 19, 2023 <div class="week"><span class="tooltip"><a href="https://www.youtube.com/@DigitalSpaceport" target="_blank"></a><fieldset><a href="https://www.youtube.com/@DigitalSpaceport" target="_blank"><img width="300px" src="ads/20230813.png" alt="Digital Spaceport" title="Digital Spaceport"></a><legend></legend></fieldset></span></div></h3>
<ul>
	<li class="weekday">SATURDAY • 08/19/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/youtube.png"> <a href="https://twitter.com/gospaceport" target="_blank">Digital Spaceport</a> "LIVE: Chia GPU Plotting Bladebit 128GB Testing + Chia Client RC6 Testing" <a href="https://twitter.com/gospaceport/status/1693026375253324036?s=20" target="_blank">Source</a> • <a href="https://www.youtube.com/watch?v=C0ZMikJ8QgI" target="_blank">Watch</a> • <a href="https://shop.digitalspaceport.com/?utm_medium=product_shelf&amp;utm_source=youtube&amp;utm_content=YT-AAE-QftT-60eFcUEB0enfDvQaiv4QLn6reepPZQpLv-hDUCxUMjEDq56nZPAHcRdgVVClyTfQnuFbwXniBSAnweP1D7gRCL5452GQY82M3Py5PgX-7PMuf2tvc4xHscJGT1x9Ve6nXYF_r5E5KxFOH_MyZcoODcYMWbrKgYLQnu0EuZi7OFPGM9b" target="_blank">DSP Store</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/youtube.png"> <a href="https://twitter.com/monkeyzoo" target="_blank">@monkeyzoo</a> releases 3 new videos on YouTube: How to Enable Chia Asset Token CATs, How to buy an NFT on the Chia Blockchain, &amp; How to create a Chia blockchain desktop wallet version 2. <a href="https://www.youtube.com/@monkeyzoo6698/videos" target="_blank">Monkeyzoo YouTube</a></li>
	<hr class="daydivide">
	<li class="weekday">FRIDAY • 08/18/2023</li>
	<hr class="daydivide">
	<li class="weekday">THURSDAY • 08/17/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/youtube.png"> <a href="https://twitter.com/VoskCoin" target="_blank">@VoskCoin</a> releases new video "How I am Earning MORE Passive Income with my Evergreen Miner HDD Chia XCH Farmers!" <a href="https://www.youtube.com/watch?v=iuuWA6271cc" target="_blank">Watch</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/spaces.png"> <span style="color:#8C52FE">Twitter Space</span> - Hosted by <a href="https://twitter.com/anewformofmusic" target="_blank">Edward</a> "🌱 Weddings , Chat and The Great Wall Of Chia 6PM LA Time #ArtThursday" on Thursday August 17, 2023. <a href="https://twitter.com/anewformofmusic/status/1692174157914701841?s=20" target="_blank">Play</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/chia.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/chia_project" target="_blank">Chia Network</a> posts new blog entry "Forked Paths: Decoding Blockchain Forks" <a href="https://www.chia.net/2023/08/17/forked-paths-decoding-blockchain-forks/" target="_blank">Blog</a></li>
	<hr class="daydivide">
	<li class="weekday">WEDNESDAY • 08/16/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/steppsr" target="_blank">@steppsr</a> (me) released some new merch products on XDTEES. <a href="https://xdtees.printify.me/products/1" target="_blank">XDTEES</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/ProofOfSynthNFT" target="_blank">SynthAndy.xch</a> posts new page to the ChiFi Degens site that is a fantastic intro into <a href="https://www.chifidegens.xyz/chia" target="_blank">Why Chia?</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/michaeltaylor3d" target="_blank">@michaeltaylor3d</a> releases new development tool: DataLayer Mirror Tools! Collection of higher level abstractions that make creating/managing/deleting your datalayer mirrors a little bit easier. <a href="https://twitter.com/michaeltaylor3d/status/1691860850062094633?s=20" target="_blank">Source</a> • <a href="https://www.npmjs.com/package/chia-datalayer-mirror-tools" target="_blank">chia-datalayer-mirror-tools</a></li>
	<hr class="daydivide">
	<li class="weekday">TUESDAY • 08/15/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/SlowestTimelord" target="_blank">@SlowestTimelord</a> teases new site: XCH.ninja! What will it be? <a href="https://xch.ninja/" target="_blank">XCH.ninja</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/chia.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/chia_project" target="_blank">Chia Network</a> posts new blog entry "What is Blockchain for “Enterprise”?" <a href="https://www.chia.net/2023/08/15/what-is-blockchain-for-enterprise/" target="_blank">Blog</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/SlowestTimelord" target="_blank">@SlowestTimelord</a> announces "ChiaLinks has a new Developers section! And sub-sections for DataLayer and WalletConnect specific resources. #Chia" <a href="https://chialinks.com/developers/" target="_blank">Developers Page</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/MayorAbandoned" target="_blank">@MayorAbandoned</a> announces "A NFT project built on the Chia Blockchain consisting of 30 rows and 14 columns of 64px X 64px images. NFT owners have the ability to change the image on this page by proving their ownership." <a href="https://thegreatwallofchia.com/" target="_blank">The Great Wall of Chia</a></li>
	<hr class="daydivide">
	<li class="weekday">MONDAY • 08/14/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/michaeltaylor3d" target="_blank">@michaeltaylor3d</a> announces "Getting your NFT collection on #Chia DataLayer is now just 2 steps!". 1) Use Sprout tool and deploy your entire collection on datalayer in just a few mins. 2) Sign up for a free account at Datalayer Storage and claim your free mirror. <a href="https://www.npmjs.com/package/chia-sprout-cli" target="_blank">chia-sprout-cli</a> • <a href="https://datalayer.storage/" target="_blank">Datalayer Storage</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/spaces.png"> <span style="color:#8C52FE">Twitter Space</span> - Hosted by <a href="https://twitter.com/DracattusDev" target="_blank">@DracattusDev</a> "🌱Chia - The World’s Most Decent. &amp; Secure Blockchain - #BTC v2" on Sunday August 13, 2023 at 6:00 PM UTC. <a href="https://twitter.com/DracattusDev/status/1691050275480457217?s=20" target="_blank">Play</a></li>
	<hr class="daydivide">
	<li class="weekday">SUNDAY • 08/13/2023</li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/MrDennisV" target="_blank">@MrDennisV</a> releases npm "chia-dl-file-store" a Node.js package that provides functionality for interacting with Chia blockchain's DataLayer to manage files. <a href="https://www.npmjs.com/package/chia-dl-file-store" target="_blank">chia-dl-file-store</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/youtube.png"> <a href="https://twitter.com/gospaceport" target="_blank">Digital Spaceport</a> "Chia Bladebit 128GB RAM GPU Plot Testing! Hard Drive Mining and Farming" <a href="https://twitter.com/gospaceport/status/1690896128785653761?s=20" target="_blank">Source</a> • <a href="https://www.youtube.com/watch?v=CNc4cWHJmdQ" target="_blank">Watch</a> • <a href="https://shop.digitalspaceport.com/?utm_medium=product_shelf&amp;utm_source=youtube&amp;utm_content=YT-AAE-QftT-60eFcUEB0enfDvQaiv4QLn6reepPZQpLv-hDUCxUMjEDq56nZPAHcRdgVVClyTfQnuFbwXniBSAnweP1D7gRCL5452GQY82M3Py5PgX-7PMuf2tvc4xHscJGT1x9Ve6nXYF_r5E5KxFOH_MyZcoODcYMWbrKgYLQnu0EuZi7OFPGM9b" target="_blank">DSP Store</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/microphone.png"> <a href="https://twitter.com/Quirky_Giraffes" target="_blank">@Quirky_Giraffes</a> releases Quirky Giraffes 2.0 collection! Offers are already up so go grab some for yourself! <a href="https://mintgarden.io/collections/quirky-giraffes-2.0-col1hw37gqd64mfejpt26r4ga37qgnaudqt3c7javemphdc4qyntedssmxxmwr" target="_blank">2.0 Collection</a></li>
	<li class="post"><img width="15px" src="https://thisweekinchia.com/assets/icons/globe.png"> <img width="15px" src="https://thisweekinchia.com/assets/icons/spaces.png"> <span style="color:#8C52FE">Twitter Space</span> - Hosted by <a href="https://twitter.com/monkeyzoo" target="_blank">@monkeyzoo</a> "🌱Chia Royalties Guaranteed🌱 New L1 #NFTs are back 🔥🔥" on Sunday August 13, 2023 at 6:00 PM UTC. <a href="https://twitter.com/monkeyzoo/status/1690785389164797952?s=20" target="_blank">Play</a></li>
	<hr class="daydivide">
</ul>

<blockquote>
	<a href="https://www.spacescan.io/"><img class="weeklyhighlightbanner" src="assets/images/spacescan.png"></a>
	<span style="color:#8C52FE">Weekly Highlight:</span> <span style="color:#00AA33">Spacescan</span>! A well deserving core community member providing a valuable service to everyone with a blockchain explorer, charts, CAT &amp; NFT explorer, tools, API, and recently Offer files. Join me in showing some love if you want: <span style="color:#00CC11">xch1a6cd558gqsz2hch5pt0l8mx7zhavf32q5lyde09zjtqcmkelr9ns59k0j8</span> or see their <a href="https://www.spacescan.io/support-us" target="_blank">Support page</a>. <span style="color:#00AA33">💗</span>
	<!-- <br><br> -->
	<img class="weeklyhighlight" src="https://thisweekinchia.com/donations/20230813.png">
</blockquote>
				
<hr>
"""

soup = BeautifulSoup(html, 'html.parser')

weeks_data = []

week_elements = soup.find_all('h3')
for week_element in week_elements:
    week_data = {}

    week_dates_text = week_element.text.strip()
    week_dates_match = re.search(r'Week of (.+?) - (.+?) Advertisement', week_dates_text)
    if week_dates_match:
        week_data['startdate'] = week_dates_match.group(1)
        end_date_parts = week_dates_match.group(2).split(' - ')[-1].split('/')
        end_date = f"{int(end_date_parts[0]):02d}/{int(end_date_parts[1]) + 7:02d}/{end_date_parts[2]}"
        week_data['enddate'] = end_date

    post_elements = week_element.find_next_sibling('ul').find_all('li', class_='post')
    posts = []

    for post_element in post_elements:
        print(post_element)
        post_data = {}

        date_parts = post_element.find_previous('li', class_='weekday').text.split(' • ')
        post_data['date'] = date_parts[1]

        icons = [img['src'].split('/')[-1].split('.')[0] for img in post_element.find_all('img')]
        post_data['icons'] = icons

        title = ""
        title_elements = post_element.find_all(text=True, recursive=False)
        for element in title_elements:
            if element.name == 'a':
                break
            title += element.strip()
        post_data['title'] = title
        print(title)

        creator_element = post_element.find('a')
        if creator_element:
            creator_name = creator_element.text.strip()
            creator_link = creator_element['href']
            post_data['handle'] = [creator_name, creator_link]

        link_elements = post_element.find_all('a')
        links = []
        for link_element in link_elements:
            link_text = link_element.text
            link_url = link_element['href']
            links.append([link_text, link_url])
        post_data['links'] = links

        posts.append(post_data)

    week_data['posts'] = posts
    weeks_data.append(week_data)

yaml_data = {'weeks': weeks_data}

with open('output.yaml', 'w') as yaml_file:
    yaml.dump(yaml_data, yaml_file, default_flow_style=None)