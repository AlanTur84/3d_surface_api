let scene, camera, renderer, terrain;

function init() {
    // Scene setup
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(1, 1, 1);
    scene.add(directionalLight);

    // Camera position
    camera.position.z = 5;
}

function visualizeDataset(features) {
    // Remove existing terrain
    if (terrain) scene.remove(terrain);
    
    // Convert features to vertices
    const vertices = features.map(f => [
        f.geometry.coordinates[0] / 10,  // X: longitude
        f.geometry.coordinates[1] / 10,  // Y: latitude 
        f.geometry.coordinates[2] / 1000 // Z: elevation
    ]);

    // Create geometry
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices.flat(), 3));

    // Generate terrain mesh
    const indices = new Delaunator(vertices.map(v => [v[0], v[1]])).triangles;
    geometry.setIndex(indices);
    geometry.computeVertexNormals();

    const material = new THREE.MeshPhongMaterial({
        color: 0x00ff00,
        wireframe: false,
        flatShading: true
    });

    terrain = new THREE.Mesh(geometry, material);
    scene.add(terrain);

    // Adjust camera
    const box = new THREE.Box3().setFromObject(terrain);
    const size = box.getSize(new THREE.Vector3()).length();
    camera.position.z = size * 1.5;
    
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
}

// Initialize on load
window.onload = init;