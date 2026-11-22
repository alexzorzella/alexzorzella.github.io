import * as THREE from 'three';

import { MapControls } from 'three/addons/controls/MapControls.js';

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

createFramedPiece(scene, 'public/art/00_illustrations/1_sunset_drive.png')

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

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );
}

function createFramedPiece(scene, artwork_src, scale=2, inner_border=0.25, frame_border=0.1) {
    const loader = new THREE.TextureLoader();

    const artwork_texture = loader.load(artwork_src, () => {
        const width = artwork_texture.width;
        const height = artwork_texture.height;
        const aspect_ratio = width / height;
        const final_width = scale * aspect_ratio;
        const final_height = scale;

        const artwork_geometry = new THREE.PlaneGeometry(final_width, final_height);
        const artwork_material = new THREE.MeshBasicMaterial({ map: artwork_texture });
        const artwork = new THREE.Mesh(artwork_geometry, artwork_material);

        artwork_texture.minFilter = THREE.NearestMipmapNearestFilter;
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
    });
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
    parent=null) {
    const geometry = new THREE.BoxGeometry(width, height, depth);
    const material = new THREE.MeshBasicMaterial();

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