import * as THREE from 'three';

import { MapControls } from 'three/addons/controls/MapControls.js';

const DATA = {
	"time_travel_cat": {title: "Time Travel Cat", date_created: "2026/06/01", description: "Tim and his wife Laura in her original body."},
	"rocco_and_elena_post_time_travel": {title: "Rocco and Elena Post Time Travel", date_created: "2026/06/01", description: "Rocco and Elena after their time travelling adventure in their Toyota Corolla."},
	"rocco_and_elena": {title: "Rocco and Elena", date_created: "2026/06/01", description: "Rocco and Elena at the very beginning of their time travelling adventure in their Toyota Corolla."},
	"meowna_lisa": {title: "Meowna Lisa", date_created: "2026/06/01", description: "She likes drinking hot chocolate every once in a while"},
	"legally_blonde_movie_night": {title: "Legally Blonde Movie Night", date_created: "2026/06/01", description: "If a machine has good taste in media, does it mean that it's alive?"},
	"frog_genie_and_tess": {title: "Frog, Genie, And Tess", date_created: "2026/06/01", description: "Tessa Pacific, holding the baseball summoning bat, and Frogman (Eun Nayar), at the beginning of the Quest To Find the Exit."},
	"bartholomew_and_scranklet": {title: "Bartholomew And Scranklet", date_created: "2026/06/01", description: "Bartholomew (left) and Skranklet (right) pose for a picture (taken by a French passerby) in front of The Louvre before they heist it"},
	"siiva_4": {title: "SiIVa", date_created: "2026/06/01", description: "Science has proven that there is always a higher quality track than the last. SiIvaGunner's peer reviews skip academia and ask the public. SiIVa's Australia/Mongolia/Brazil tour was their most successful, being nominated for various awards, but eventually winning 'Best in Quality'. After demand from the public increased post-ceremony, the tour was extended to Canada and the United States of America.From Wikipedia (https://en.wikipedia.org/wiki/SiIvaGu...) under Creative Commons Attribution CC-BY-SA 3.0 (https://creativecommons.org/licenses/...)"},
	"knights_of_the_grand_2": {title: "Knights of the Grand Table", date_created: "2026/06/01", description: "In August of 2005, SiIvaGunner released their third compilation album to the public. Three years after their second release, the public had assumed they had left the scene. Millions watched the premiere live, flooding the streets of Paris, where the event was held live. While SiIvaGunner's Grand Day Out explored the line between rip and art and SiIvaGunner Fans When the Channel Is Ending for the 37th Time showcased longer tracks than ever before, SiIvaGunner's Knights of the Round Table is the quest to find the highest quality rips to date. From Wikipedia (https://en.wikipedia.org/wiki/SiIvaGu...) under Creative Commons Attribution CC-BY-SA 3.0 (https://creativecommons.org/licenses/...)"},
	"high_quality_hotline": {title: "High Quality Hotline", date_created: "2026/06/01", description: "The High Quality storage facility was constructed with hundreds of landlines in preparation for the High Quality Shortage. Call, toll-free, at 1 800 555 0001"},
	"grand_halation": {title: "Grand Halation", date_created: "2026/06/01", description: "..."},
	"wedding_ring": {title: "Wedding Ring", date_created: "2026/06/01", description: "Eloise bought her wedding dress at Lowe's and Jacob ordered the wedding rings at Michael's."},
	"toaster": {title: "Toaster", date_created: "2026/06/01", description: "A toaster with a man's soul. He sees through a CCTV camera, has a chainsaw for an arm, and runs everything on ten Intel® Core™ i7-7700 Processors hooked up in parallel. His torso is a car battery. His consciousness requires no computational power to maintain."},
	"taylor": {title: "Taylor", date_created: "2026/06/01", description: "Taylor commits many federal crimes on her pet ostrich."},
	"snuffler_s_bluff_ratman_at_sign": {title: "Snuffler's Bluff and Ratman At Sign", date_created: "2026/06/01", description: "Snuffler's Bluff National Park: privately funded, publicly owned."},
	"snuffler_s_bluff": {title: "Snuffler's Bluff", date_created: "2026/06/01", description: "That's rare, it's just walking by."},
	"sharkman": {title: "Sharkman", date_created: "2026/06/01", description: "The president of WCO (World Circuit Organization) 2030 shakes hands with a sharkman."},
	"refrigerator": {title: "Refrigerator", date_created: "2026/06/01", description: "The first prototypes of the toaster man's mobile features."},
	"ratman_models": {title: "Ratman Model Catalogue", date_created: "2026/06/01", description: "Funding for the exoskeletons was generously provided by REDACTED."},
	"ratman_5": {title: "Ratman 5", date_created: "2026/06/01", description: "This is not Ratman."},
	"ratman_2": {title: "Ratman 2", date_created: "2026/06/01", description: "An early model: most of the components are not functional."},
	"ratman_1": {title: "Ratman 1", date_created: "2026/06/01", description: "The earliest functional model. In total, it weighs 1 ton and cost nearly $530,000 to manufacture. Funding was generously provided by REDACTED."},
	"rat_slayer": {title: "Rat Slayer", date_created: "2026/06/01", description: "This left-handed sleeper agent is hired by contract. While activated, they are supposedly amoral. They handle supernatural contracts often."},
	"rat_concept": {title: "Rat Concept", date_created: "2026/06/01", description: "These rats support the arts."},
	"metafight_wisdom_chicken": {title: "Wisdom Chicken", date_created: "2026/06/01", description: "Early scene involving the Bone Zone's Wisdom Chicken."},
	"metafight_unused_menu_sprites": {title: "Unused Metafight Menu Sprites", date_created: "2026/06/01", description: "AP Gaming was discontinued in the United States after a group of Washington students all scored 100% on the exam: they were deemed too powerful."},
	"metafight_menu_sprites": {title: "Metafight Menu Sprites", date_created: "2026/06/01", description: "The document declares itself as valid LOL"},
	"metafight_menu_art_bandage": {title: "Metafight Menu Art Bandage", date_created: "2026/06/01", description: "Patient 15"},
	"metafight_lightning": {title: "Metafight Lightning Splash Image", date_created: "2026/06/01", description: "Black t-shirt, pants, socks, shoes, and hair dye. Whoa."},
	"metafight_bone_zone_master": {title: "Bone Zone Master", date_created: "2026/06/01", description: "The Third Bone Zone Master."},
	"inquiry": {title: "Inquiry", date_created: "2026/06/01", description: "Inquiry"},
	"iced_tea": {title: "Iced Tea", date_created: "2026/06/01", description: "Frieren enjoys a timeless activity: lounging while drinking tea."},
	"her_cooking": {title: "Her Cooking", date_created: "2026/06/01", description: "Don't let the food burn."},
	"gaming_truck": {title: "Gaming Truck", date_created: "2026/06/01", description: "Remaster"},
	"elesh_morn": {title: "Elesh Morn", date_created: "2026/06/01", description: "She also likes hot chocolate LOL"},
	"danitha": {title: "Danitha", date_created: "2026/06/01", description: "Danitha and friends"},
	"court": {title: "Court", date_created: "2026/06/01", description: "Plea: not even close to being guilty it's funny"},
	"color_image": {title: "Color Image", date_created: "2026/06/01", description: "It's Terry's hairstyle lol"},
	"check_in_montage": {title: "Check-In Montage", date_created: "2026/06/01", description: "The original drawing is over a meter long: this is the cut down version that I used as reference for the digitally-drawn banner."},
	"campfire": {title: "Campfire", date_created: "2026/06/01", description: "Hello, Bass Fishing. I would like to purchase a fishing rod. Can you point me to your heat resistant section?"},
	"cameraman_no_1": {title: "Cameraman No. 1", date_created: "2026/06/01", description: "Karen Ley is a thirty five year old photographer, journalist, and cameraman."},
	"tashana_first_look": {title: "Tashana", date_created: "2026/06/01", description: "Tashana Mondrian is a dancer and martial artist that carries a mop on her back."},
	"starlight_serenade": {title: "Starlight Serenade", date_created: "2026/06/01", description: "Slate orders a meal with the Wisdom Chicken (left), June approaches the elevator button (right)"},
	"square": {title: "Square", date_created: "2026/06/01", description: "Womanspider began as an ordinary spider, but was bit by a woman and now fights crime using a sword and shield. The haircut was by request"},
	"slate_sketches": {title: "Slate Sketches", date_created: "2026/06/01", description: "Founder of the Friday Night Knockout Tournament."},
	"lola": {title: "Lola", date_created: "2026/06/01", description: "Do not feed the... huh?"},
	"laura_sketches": {title: "Laura Sketches", date_created: "2026/06/01", description: "Laura and acquaintances before her career in the Friday Night Knockout Tournament. Naturally blonde and Canadian, she lives with her parents in Brazil and dyes her hair every week."},
	"godot_sketches": {title: "Godot Sketches", date_created: "2026/06/01", description: "Godot, hailing from Singapore, is a high school student that now finds himself in the body of a chicken."},
	"business_casual": {title: "Business Casual", date_created: "2026/06/01", description: "Someone wearing a Friday Night Knockout Tournament themed jacket."},
	"acid_crest_labs_cover": {title: "Acid Crest Labs Cover", date_created: "2026/06/01", description: "Sharon owns two green turtlenecks she purchased at Nicole's Hardware and Workwear on discount. They have both lasted her over five years."},
	"of_rats_and_men": {title: "Of Rats And Men", date_created: "2026/06/01", description: "The first and second designs for Jerome the rat."},
	"momo_sgt_pepper": {title: "Momo Sgt. Pepper", date_created: "2026/06/01", description: "Momo joins Sgt. Pepper's Lonely Hearts Club Band after meeting the Beatles."},
	"duolingo": {title: "Duolingo", date_created: "2026/06/01", description: "Duolingo at the Bob Ross studio."},
	"conversation": {title: "Conversation", date_created: "2026/06/01", description: "A casual discussion between Slate and June, the president of the Bone Republic."},
	"4_suplex_final": {title: "Suplex", date_created: "2026/06/01", description: "Slate suplexing Laura."},
	"3_check_in_final": {title: "Check-In", date_created: "2026/06/01", description: "A state governmental building repurposed to act as the Friday Night Knockout Tournament office."},
	"2_nap_final": {title: "Nap", date_created: "2026/06/01", description: "Rocco and Elena, five years after Rocco takes a position as a cameraman for the Friday Night Knockout Tournament."},
	"1_sunset_drive": {title: "Beautiful Saturday", date_created: "2026/06/01", description: "Pictured from left to right: Unknown Corrupted Individual, Unknown Driver, Unknown Mole Person, June (president of the Bone Republic), and Tim."},
	"0_gar": {title: "Gar", date_created: "2026/06/01", description: "The Gar-Man can be found in Crater Lake National Park."},
	"bike_path": {title: "Bike Path", date_created: "2026/06/09", description: "It's all outlined in here, take a look"},
	"running_hawaiian_shirt": {title: "Running", date_created: "2026/06/10", description: "Always be careful in areas with vampires: bring a friend and prepare your escape."},
	"ratman": {title: "Ratman", date_created: "2026/07/16", description: ""},
	"sabrina_carpenter": {title: "Sabrina Carpenter", date_created: "2026/07/16", description: ""},
	"sabreama_carpenter": {title: "Sabreama Carpenter", date_created: "2026/07/16", description: ""},
	"artemis_ii": {title: "Artemis II", date_created: "2026/07/17", description: "nodesc"},
	"siiva_2": {title: "SiIvaGunner Fans When the Channel Is Ending For the 37th Time", date_created: "2026/07/17", description: "nodesc"},
	"siiva_6": {title: "SiIva6unner's This Mix Contains a High Concentration of Quality Music", date_created: "2026/07/17", description: "nodesc"},
	"siiva_3": {title: "SiIvaGunner's Knights of the Grand Table", date_created: "2026/06/17", description: "nodesc"},
	"siiva_5": {title: "SiIvaGunner's High Quality Hotline", date_created: "2026/06/17", description: "nodesc"},
	"siiva_0": {title: "SiIvaGunner's Grand Halation", date_created: "2026/06/17", description: "nodesc"},
	"xenomorph_leaping": {title: "Xenomorph Leaping", date_created: "2026/11/22", description: ""},
	"breaking_bad_valorant_crossover_blown_up": {title: "Breaking Bad Valorant Crossover Blown Up", date_created: "2026/11/22", description: ""},
	"laura_portrait": {title: "Laura Portrait", date_created: "2026/11/22", description: ""},
	"great_catch": {title: "Great Catch", date_created: "2026/11/22", description: ""},
	"bus_stop_question": {title: "Bus Stop Question", date_created: "2026/11/22", description: ""},
	"swerve": {title: "Swerve", date_created: "2026/11/22", description: ""},
	"socrates_plugin_logo": {title: "Socrates Plugin Logo", date_created: "2026/11/22", description: ""},
	"thursday_night_takeout_marie_curries_flavor_cover": {title: "Thursday Night Takeout Marie Curries Flavor Cover", date_created: "2026/11/22", description: ""},
	"networking_cover": {title: "Networking Cover", date_created: "2026/11/22", description: ""},
	"economics_cover": {title: "Economics Cover", date_created: "2026/11/22", description: ""},
	"rendered_greg": {title: "Rendered Greg", date_created: "2026/11/22", description: ""},
	"os_cover": {title: "Os Cover", date_created: "2026/11/22", description: ""},
	"operating_systems_ii_cover": {title: "Operating Systems Ii Cover", date_created: "2026/11/22", description: ""},
	"operating_systems_cover": {title: "Operating Systems Cover", date_created: "2026/11/22", description: ""},
	"valorant": {title: "Valorant", date_created: "2026/11/22", description: ""},
	"labs_cover": {title: "Labs Cover", date_created: "2026/06/17", description: ""},
	"tree": {title: "Tree", date_created: "2026/11/22", description: ""},
	"tahoe": {title: "Tahoe", date_created: "2026/11/22", description: ""},
	"poncho": {title: "Poncho", date_created: "2026/11/22", description: ""},
	"plan": {title: "Plan", date_created: "2026/11/22", description: ""},
	"lang": {title: "Lang", date_created: "2026/11/22", description: ""},
	"introspect": {title: "Introspect", date_created: "2026/11/22", description: ""},
	"bag": {title: "Bag", date_created: "2026/11/22", description: ""},

}

function main() {
    let controls;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

    scene.background = new THREE.Color(0xf2e5df);

    const renderer = new THREE.WebGLRenderer({antialias: true});
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    controls = new MapControls( camera, renderer.domElement );

    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    controls.screenSpacePanning = true;

    controls.minDistance = 1;
    controls.maxDistance = 10;

    controls.zoomToCursor = true;

    // controls.maxPolarAngle = Math.PI / 2;

    const dirLight1 = new THREE.DirectionalLight( 0xffffff, 3 );
    dirLight1.position.set( 1, 1, 1 );
    scene.add( dirLight1 );

    const dirLight2 = new THREE.DirectionalLight( 0x002288, 3 );
    dirLight2.position.set( - 1, - 1, - 1 );
    scene.add( dirLight2 );

    const ambientLight = new THREE.AmbientLight( 0x555555 );
    scene.add( ambientLight );

    window.addEventListener( 'resize', onWindowResize );

    //

    createObject(scene, null, 'resources/textures/beige_wall.jpg', 14, 8, 1, 0,2, 0)
    createObject(scene, null, 'resources/textures/dark_wood.jpg', 3, 0.7, 0.8, 0, -1.75, 5.7);

    const url = new URL(window.location.href);
    const initial_query = url.searchParams.get("q");

    if(initial_query != null) {
        createFramedPiece(scene, decodeURIComponent(initial_query))
    }

    // const floor_geometry = new THREE.BoxGeometry(10, 0.5, 10);
    // const floor_material = new THREE.MeshBasicMaterial({ color: 0xf2e5df });
    // const floor = new THREE.Mesh(floor_geometry, floor_material);
    // floor.position.set(0, -2, 0)
    // scene.add(floor);

    camera.position.z = 5;

    function animate(time) {
        controls.update();

        renderer.render(scene, camera);
    }

    renderer.setAnimationLoop(animate);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );
}

async function createFramedPiece(scene, artwork_src, scale=2, inner_border=0.25, frame_border=0.1) {
    const query = artwork_src.split("/");
    const artwork_reference_id = query[query.length - 1].replace('.png','');

    console.log(artwork_reference_id);
    console.log(DATA[artwork_reference_id]);

    const loader = new THREE.TextureLoader();

    const font = new FontFace("imperial", "url(/public/fonts/imperial.woff2)")

    const [artwork_texture, _] = await Promise.all([
            new Promise( (resolve, reject) => {
            const texture = loader.load(artwork_src, () => { resolve(texture) })
        }),
        font.load()
    ])

    const width = artwork_texture.width;
    const height = artwork_texture.height;
    const aspect_ratio = width / height;
    const final_width = scale * aspect_ratio;
    const final_height = scale;

    const artwork_geometry = new THREE.PlaneGeometry(final_width, final_height);
    const artwork_material = new THREE.MeshBasicMaterial({ map: artwork_texture });
    const artwork = new THREE.Mesh(artwork_geometry, artwork_material);

    artwork_texture.minFilter = THREE.LinearMipmapNearestFilter;
    artwork_texture.colorSpace = THREE.SRGBColorSpace;

    scene.add(artwork);

    const frame_origin_y = 1
    const frame_origin_z = 0.5

    const frame_width = final_width + inner_border * 2
    const frame_height = final_height + inner_border * 2
    const frame_depth = 0.2

    const frame = createObject(scene, new THREE.Color(0xf5eae4), null, frame_width, frame_height, frame_depth, 0, frame_origin_y, frame_origin_z);
    createObject(scene, null, 'resources/textures/dark_wood.jpg', frame_width + frame_border * 2, frame_border, frame_depth + 0.05, 0, frame_height / 2 + frame_border / 2, 0, frame);
    createObject(scene, null, 'resources/textures/dark_wood.jpg', frame_width + frame_border * 2, frame_border, frame_depth + 0.05, 0, -(frame_height / 2 + frame_border / 2), 0, frame);
    createObject(scene, null, 'resources/textures/dark_wood.jpg', frame_border, frame_height, frame_depth + 0.05, -(frame_width / 2 + frame_border / 2), 0, 0, frame);
    createObject(scene, null, 'resources/textures/dark_wood.jpg', frame_border, frame_height, frame_depth + 0.05, frame_width / 2 + frame_border / 2, 0, 0, frame);

    frame.add(artwork);
    artwork.position.set(0, 0, frame_depth / 2 + 0.01);

    const canvas = document.createElement('canvas')
    const context = canvas.getContext('2d')
    canvas.width = 1000
    canvas.height = 1410
    context.fillStyle = "#f5eae4"
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "#000000";
    context.font = "normal 900 100px imperial"
    context.fillText(DATA[artwork_reference_id].title, 40, 120)
    context.font = "80px imperial"
    context.fillText(DATA[artwork_reference_id].description, 40, 220)

    const info_texture = new THREE.CanvasTexture(canvas);

    const info_width = 1 / 2
    const info_height = 1.41 / 2

    const info_geometry = new THREE.PlaneGeometry(info_width, info_height);
    const info_material = new THREE.MeshBasicMaterial({ map: info_texture });
    const info_object = new THREE.Mesh(info_geometry, info_material);

    scene.add(info_object);
    frame.add(info_object);

    info_object.position.set(frame_width / 2 + info_width / 2 + frame_border + 0.25, -(frame_height / 2 + frame_border) + info_height / 2, 0.01);

    // const glass_material = new THREE.MeshPhysicalMaterial({ roughness: 0, transmission: 1, thickness: 0 });
    // const glass = createObject(scene, null, null, frame_width, frame_height, 0.025, 0, 0, 0.1, frame, glass_material);
    // glass.material.set(glass_material);
}

function createObject(
    scene,
    color=null,
    texture_src=null,
    width=1,
    height=1,
    depth=1,
    x=0,
    y=0,
    z=0,
    parent=null,
    material=null) {
    const geometry = new THREE.BoxGeometry(width, height, depth);

    if(material == null) {
        material = new THREE.MeshBasicMaterial();
    }

    if(color != null) {
       material.color = color;
    } else if(texture_src != null) {
        const loader = new THREE.TextureLoader();
        const texture = loader.load(texture_src);
        console.log(texture);
        texture.colorSpace = THREE.SRGBColorSpace;
        material.map = texture;
    }

    const object = new THREE.Mesh(geometry, material);

    scene.add(object);

    if(parent != null) {
        parent.add(object);
    }

    object.position.set(x, y, z);

    return object;
}

main();