let terrainMesh = null;

function createTerrainMesh(features) {
    // Convert features to scaled vertices
    const vertices = features.map(f => {
        const [lon, lat, elev] = f.geometry.coordinates;
        return {
            x: lon / 10,
            y: lat / 10,
            z: elev / 1000
        };
    });

    // Create geometry
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(vertices.flatMap(v => [v.x, v.y, v.z]));
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.computeBoundingBox();

    // Create delaunay triangles
    const indices = Delaunator.from(
        vertices.map(v => [v.x, v.y])
    ).triangles;
    
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    // Create material
    const material = new THREE.MeshPhongMaterial({
        color: 0x00ff00,
        wireframe: true,
        side: THREE.DoubleSide
    });

    return new THREE.Mesh(geometry, material);
}

async function processDataset() {
    const file = document.getElementById('dataset').files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/dataset', { method: 'POST', body: formData });
        const data = await response.json();
        
        if(terrainMesh) scene.remove(terrainMesh);
        
        terrainMesh = createTerrainMesh(data.features);
        scene.add(terrainMesh);
        
        // Adjust camera
        const box = new THREE.Box3().setFromObject(terrainMesh);
        const size = box.getSize(new THREE.Vector3()).length();
        camera.position.z = size * 2;
        
        renderer.render(scene, camera);
        
    } catch (error) {
        console.error('Error processing dataset:', error);
    }
}

// Initialize scene with lights
function initThree() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    
    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    renderer.setSize(window.innerWidth*0.8, window.innerHeight*0.6);
    document.getElementById('model-container').appendChild(renderer.domElement);
}