// Advanced thinking visualization
class ThinkingVisualization {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container with ID ${containerId} not found`);
            return;
        }
        
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight || 150;
        this.nodes = [];
        this.connections = [];
        this.maxNodes = 20;
        this.nodeColors = ['#10a37f', '#19c37d', '#25d195', '#34d399'];
        
        // Set container style
        this.container.style.position = 'relative';
        this.container.style.height = `${this.height}px`;
        this.container.style.backgroundColor = '#343541';
        this.container.style.borderRadius = '8px';
        this.container.style.overflow = 'hidden';
        
        // Initialize
        this.init();
    }
    
    init() {
        // Clear container
        this.container.innerHTML = '';
        this.nodes = [];
        this.connections = [];
        
        // Create initial nodes
        this.addNode();
        
        // Start animation
        this.animate();
    }
    
    addNode() {
        if (this.nodes.length >= this.maxNodes) {
            return;
        }
        
        const x = Math.random() * this.width;
        const y = Math.random() * this.height;
        const size = 5 + Math.random() * 10;
        const color = this.nodeColors[Math.floor(Math.random() * this.nodeColors.length)];
        const speed = 0.2 + Math.random() * 0.5;
        const direction = Math.random() * Math.PI * 2;
        
        const nodeEl = document.createElement('div');
        nodeEl.className = 'thinking-node';
        nodeEl.style.width = `${size}px`;
        nodeEl.style.height = `${size}px`;
        nodeEl.style.backgroundColor = color;
        nodeEl.style.left = `${x}px`;
        nodeEl.style.top = `${y}px`;
        
        this.container.appendChild(nodeEl);
        
        const node = {
            el: nodeEl,
            x,
            y,
            size,
            color,
            speed,
            direction,
            connections: []
        };
        
        this.nodes.push(node);
        
        // Connect to some existing nodes
        if (this.nodes.length > 1) {
            const connectionsCount = Math.min(3, this.nodes.length - 1);
            for (let i = 0; i < connectionsCount; i++) {
                const targetIndex = Math.floor(Math.random() * (this.nodes.length - 1));
                const target = this.nodes[targetIndex];
                
                // Don't connect to the same node twice
                if (node.connections.includes(target)) {
                    continue;
                }
                
                this.createConnection(node, target);
            }
        }
        
        return node;
    }
    
    createConnection(node1, node2) {
        const connectionEl = document.createElement('div');
        connectionEl.className = 'thinking-connection';
        this.container.appendChild(connectionEl);
        
        const connection = {
            el: connectionEl,
            node1,
            node2
        };
        
        this.connections.push(connection);
        node1.connections.push(node2);
        node2.connections.push(node1);
        
        return connection;
    }
    
    updateConnections() {
        this.connections.forEach(conn => {
            const dx = conn.node2.x - conn.node1.x;
            const dy = conn.node2.y - conn.node1.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            const angle = Math.atan2(dy, dx);
            
            conn.el.style.width = `${distance}px`;
            conn.el.style.left = `${conn.node1.x}px`;
            conn.el.style.top = `${conn.node1.y + conn.node1.size / 2}px`;
            conn.el.style.transform = `rotate(${angle}rad)`;
        });
    }
    
    animate() {
        // Add new node occasionally
        if (Math.random() < 0.05 && this.nodes.length < this.maxNodes) {
            this.addNode();
        }
        
        // Move nodes
        this.nodes.forEach(node => {
            // Update position
            node.x += Math.cos(node.direction) * node.speed;
            node.y += Math.sin(node.direction) * node.speed;
            
            // Bounce off walls
            if (node.x < 0 || node.x > this.width) {
                node.direction = Math.PI - node.direction;
            }
            if (node.y < 0 || node.y > this.height) {
                node.direction = -node.direction;
            }
            
            // Keep within bounds
            node.x = Math.max(0, Math.min(this.width, node.x));
            node.y = Math.max(0, Math.min(this.height, node.y));
            
            // Update element position
            node.el.style.left = `${node.x}px`;
            node.el.style.top = `${node.y}px`;
            
            // Randomly change direction
            if (Math.random() < 0.02) {
                node.direction += (Math.random() - 0.5) * Math.PI / 2;
            }
        });
        
        // Update connections
        this.updateConnections();
        
        // Continue animation
        requestAnimationFrame(() => this.animate());
    }
    
    // Public methods
    pulse() {
        this.nodes.forEach(node => {
            node.el.style.animation = 'pulse 1s';
            setTimeout(() => {
                node.el.style.animation = '';
            }, 1000);
        });
    }
    
    addThought() {
        const node = this.addNode();
        if (node) {
            node.el.style.animation = 'pulse 1s';
            setTimeout(() => {
                node.el.style.animation = '';
            }, 1000);
        }
    }
    
    reset() {
        this.init();
    }
}

// Progress bar animation
class ProgressBar {
    constructor(containerId, duration = 5000) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            console.error(`Container with ID ${containerId} not found`);
            return;
        }
        
        this.duration = duration;
        this.startTime = null;
        this.animationId = null;
        
        // Create elements
        this.progressContainer = document.createElement('div');
        this.progressContainer.className = 'progress-container';
        
        this.progressBar = document.createElement('div');
        this.progressBar.className = 'progress-bar';
        this.progressBar.style.width = '0%';
        
        this.progressContainer.appendChild(this.progressBar);
        this.container.appendChild(this.progressContainer);
    }
    
    start() {
        this.startTime = Date.now();
        this.update();
    }
    
    update() {
        const elapsed = Date.now() - this.startTime;
        const progress = Math.min(100, (elapsed / this.duration) * 100);
        
        this.progressBar.style.width = `${progress}%`;
        
        if (progress < 100) {
            this.animationId = requestAnimationFrame(() => this.update());
        } else {
            this.onComplete();
        }
    }
    
    onComplete() {
        // Pulse effect when complete
        this.progressBar.style.animation = 'pulse 1s';
        setTimeout(() => {
            this.progressBar.style.animation = '';
        }, 1000);
    }
    
    reset() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        this.progressBar.style.width = '0%';
    }
    
    setProgress(percent) {
        this.progressBar.style.width = `${percent}%`;
    }
}

// Initialize visualizations when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Initialize thinking visualizations if containers exist
    const thinkingContainers = document.querySelectorAll('.thinking-visualization');
    thinkingContainers.forEach((container, index) => {
        window[`thinkingVis${index}`] = new ThinkingVisualization(container.id);
    });
    
    // Initialize progress bars if containers exist
    const progressContainers = document.querySelectorAll('.progress-container');
    progressContainers.forEach((container, index) => {
        window[`progressBar${index}`] = new ProgressBar(container.id);
    });
});

// Function to create a thinking visualization dynamically
function createThinkingVisualization(containerId) {
    return new ThinkingVisualization(containerId);
}

// Function to create a progress bar dynamically
function createProgressBar(containerId, duration) {
    return new ProgressBar(containerId, duration);
}
