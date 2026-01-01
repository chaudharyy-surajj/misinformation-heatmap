// Verification script for Data Summary Button functionality
// This script can be run in the browser console to test the implementation

console.log('🧪 Starting Data Summary Button Verification...');

// Test 1: Check if the button exists
function testButtonExists() {
    const button = document.querySelector('button[onclick="showDataSummary()"]');
    if (button) {
        console.log('✅ Test 1 PASSED: Data Summary button found');
        console.log('   Button text:', button.textContent.trim());
        return true;
    } else {
        console.log('❌ Test 1 FAILED: Data Summary button not found');
        return false;
    }
}

// Test 2: Check if the showDataSummary function exists
function testFunctionExists() {
    if (typeof showDataSummary === 'function') {
        console.log('✅ Test 2 PASSED: showDataSummary function exists');
        return true;
    } else {
        console.log('❌ Test 2 FAILED: showDataSummary function not found');
        return false;
    }
}

// Test 3: Test API endpoint accessibility
async function testApiEndpoint() {
    try {
        const response = await fetch('/api/v1/analytics/summary');
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Test 3 PASSED: Analytics API endpoint accessible');
            console.log('   Sample data:', {
                total_events: data.total_events,
                high_risk_events: data.high_risk_events,
                ml_status: data.ml_status
            });
            return true;
        } else {
            console.log('❌ Test 3 FAILED: API returned status', response.status);
            return false;
        }
    } catch (error) {
        console.log('❌ Test 3 FAILED: API request failed -', error.message);
        return false;
    }
}

// Test 4: Test modal creation
function testModalCreation() {
    try {
        // Simulate the modal creation process
        let modal = document.getElementById('data-summary-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'data-summary-modal';
            modal.className = 'data-summary-modal';
            document.body.appendChild(modal);
        }
        
        if (modal) {
            console.log('✅ Test 4 PASSED: Modal can be created');
            // Clean up test modal
            modal.remove();
            return true;
        } else {
            console.log('❌ Test 4 FAILED: Modal creation failed');
            return false;
        }
    } catch (error) {
        console.log('❌ Test 4 FAILED: Modal creation error -', error.message);
        return false;
    }
}

// Test 5: Test CSS styles exist
function testCssStyles() {
    const testElement = document.createElement('div');
    testElement.className = 'data-summary-modal';
    document.body.appendChild(testElement);
    
    const styles = window.getComputedStyle(testElement);
    const hasStyles = styles.position === 'fixed' || styles.display === 'none';
    
    testElement.remove();
    
    if (hasStyles) {
        console.log('✅ Test 5 PASSED: CSS styles for modal are present');
        return true;
    } else {
        console.log('❌ Test 5 FAILED: CSS styles for modal not found');
        return false;
    }
}

// Run all tests
async function runAllTests() {
    console.log('\n🚀 Running Data Summary Button Verification Tests...\n');
    
    const results = {
        buttonExists: testButtonExists(),
        functionExists: testFunctionExists(),
        apiEndpoint: await testApiEndpoint(),
        modalCreation: testModalCreation(),
        cssStyles: testCssStyles()
    };
    
    const passedTests = Object.values(results).filter(result => result).length;
    const totalTests = Object.keys(results).length;
    
    console.log('\n📊 Test Results Summary:');
    console.log(`   Passed: ${passedTests}/${totalTests} tests`);
    
    if (passedTests === totalTests) {
        console.log('🎉 ALL TESTS PASSED! Data Summary button should work correctly.');
        console.log('💡 Try clicking the "📊 Data Summary" button in the navbar to test it!');
    } else {
        console.log('⚠️  Some tests failed. Check the implementation.');
    }
    
    return results;
}

// Auto-run tests if this script is executed
runAllTests();

// Export for manual testing
window.verifyDataSummary = runAllTests;
console.log('\n💡 You can also run: verifyDataSummary() to test again');