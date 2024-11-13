// Script.js

// Reset Button
document.getElementById("resetButton").addEventListener("click", function () {
    localStorage.removeItem('sortableListOrder');  // Clear saved order
    location.reload();  // Reload the page to reset the list to original order
});

// Save function to store the current list order
function saveState(slot) {
    const order = Array.from(sortableList.children).map(item => item.innerHTML);
    localStorage.setItem(`sortableListOrder${slot}`, JSON.stringify(order));
    console.log(`Order saved in slot ${slot}:`, order);
}

// Load function to restore the list order from a specific slot
function loadState(slot) {
    const savedOrder = JSON.parse(localStorage.getItem(`sortableListOrder${slot}`));
    if (savedOrder) {
        sortableList.innerHTML = '';
        savedOrder.forEach(itemHTML => {
            const listItem = document.createElement('li');
            listItem.innerHTML = itemHTML;
            sortableList.appendChild(listItem);
        });
        console.log(`Order loaded from slot ${slot}`);
    } else {
        console.log(`No saved order found in slot ${slot}`);
    }
}

// Event listeners for save buttons
document.getElementById("save1Button").addEventListener("click", function () { saveState(1); });
document.getElementById("save2Button").addEventListener("click", function () { saveState(2); });
document.getElementById("save3Button").addEventListener("click", function () { saveState(3); });

// Event listeners for load buttons
document.getElementById("load1Button").addEventListener("click", function () { loadState(1); });
document.getElementById("load2Button").addEventListener("click", function () { loadState(2); });
document.getElementById("load3Button").addEventListener("click", function () { loadState(3); });

// Initialize SortableJS on the list element
const sortableList = document.getElementById("sortable");

Sortable.create(sortableList, {
    animation: 150, // Adds a smooth animation while dragging
    ghostClass: 'sortable-ghost', // Adds a class for the placeholder item while dragging
    onEnd: function (evt) {
        // This event is fired when the user has dropped the item
        console.log(`Item moved from index ${evt.oldIndex} to ${evt.newIndex}`);
    // Save the current order to localStorage on drop
    saveOrder();
}
});

// Function to save the current list order to localStorage
function saveOrder() {
const order = Array.from(sortableList.children).map(item => item.innerHTML);
localStorage.setItem('sortableListOrder', JSON.stringify(order));
console.log('Order saved:', order);
}

// Function to load and apply the saved order from localStorage
function loadOrder() {
const savedOrder = JSON.parse(localStorage.getItem('sortableListOrder'));
if (savedOrder) {
    sortableList.innerHTML = '';
    savedOrder.forEach(itemHTML => {
        const listItem = document.createElement('li');
        listItem.innerHTML = itemHTML;
        sortableList.appendChild(listItem);
    });
}
}

// Load the saved order when the page loads
document.addEventListener('DOMContentLoaded', loadOrder);