document.addEventListener("DOMContentLoaded", function () {
    // Elements
    const categoryDropdown = document.getElementById("category");
    const newCategoryContainer = document.getElementById("new-category-container");
    const subCategoryDropdown = document.getElementById("sub-category");
    const newSubCategoryContainer = document.getElementById("new-subcategory-container");

    /**
     * Handles category change event.
     * - Shows "New Category" input if "Other" is selected.
     * - Fetches subcategories from the backend and updates the dropdown.
     */
    function handleCategoryChange() {
        const selectedCategory = categoryDropdown.value;
        console.log("Selected Category:", selectedCategory);

        // Toggle new category input visibility
        newCategoryContainer.style.display = (selectedCategory === "Other") ? "block" : "none";

        // Clear previous subcategories
        subCategoryDropdown.innerHTML = "";

        // Fetch subcategories from Flask API
        updateSubcategories(selectedCategory)
        
    }

    function updateSubcategories(selectedCategory) {

        function appendOption(value, textContent) {
            let option = document.createElement("option");
            option.value = value;
            option.textContent = textContent;
            subCategoryDropdown.appendChild(option);
        }

        fetch(`/subcategories/${selectedCategory}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(({ name }) => appendOption(name, name));
                appendOption("Other", "Other")

                // Show newCategoryContainer if no data is returned
                newCategoryContainer.style.display = data.length === 0 ? "block" : "none";
                
                newSubCategoryContainer.style.display = (subCategoryDropdown.value === "Other") ? "block" : "none";
            })
            .catch(error => console.error("Error fetching subcategories:", error));
    }

    /**
     * Handles subcategory change event.
     * - Shows "New Subcategory" input if "Other" is selected.
     */
    function handleSubCategoryChange() {
        const selectedSubCategory = subCategoryDropdown.value;
        console.log("Selected Subcategory:", selectedSubCategory);
        newSubCategoryContainer.style.display = (selectedSubCategory === "Other") ? "block" : "none";
    }

    // Attach event listeners
    categoryDropdown.addEventListener("change", handleCategoryChange);
    subCategoryDropdown.addEventListener("change", handleSubCategoryChange);

    // Initial trigger in case of a default value
    handleCategoryChange();
});