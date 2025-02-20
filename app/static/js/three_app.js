let scene, camera, renderer, point;

function initThree() {
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth*0.8, window.innerHeight*0.6);
    document.getElementById('model-container').appendChild(renderer.domElement);

    // Add axes helper
    const axesHelper = new THREE.AxesHelper(5);
    scene.add(axesHelper);

    camera.position.z = 5;
}

function addDataPoint(lon, lat, elevation) {
    if(point) scene.remove(point);
    
    const geometry = new THREE.SphereGeometry(0.1);
    const material = new THREE.MeshBasicMaterial({color: 0xff0000});
    point = new THREE.Mesh(geometry, material);
    
    // Convert geographic coordinates to 3D space
    point.position.x = lon / 10;
    point.position.y = lat / 10;
    point.position.z = elevation / 1000;
    
    scene.add(point);
    renderer.render(scene, camera);
}

async function generateModel(event) {
    event.preventDefault();
    const lat = parseFloat(document.getElementById('lat').value);
    const lon = parseFloat(document.getElementById('lon').value);

    try {
        const response = await fetch(`/api/generate_model?lat=${lat}&lon=${lon}`);
        const data = await response.json();
        
        if(!scene) initThree();
        addDataPoint(
            data.geometry.coordinates[0],
            data.geometry.coordinates[1],
            data.properties.elevation
        );
    } catch (error) {
        console.error('Error:', error);
    }
}

// Initialize on first load
window.onload = initThree;