@IsTest
public class WeekCodesControllerTest {
    
    // This method sets up test data that will be used by the test methods.
    @TestSetup
    static void setup() {
        // Create and insert a record type for Picklist__c
        // RecordType rt = [SELECT Id FROM Picklist__c WHERE RecordTypeId = 'Daniel Cortild' LIMIT 1];
        
        // Create test Picklist__c records
        List<Picklist__c> picklistRecords = new List<Picklist__c>();
        for (Integer i = 0; i < 5; i++) {
            picklistRecords.add(new Picklist__c(
                Name = 'Week ' + i,
                Week_Code__c = 'C' + i,
                RecordTypeId = '012P5000001CUEfIAO'
            ));
        }
        insert picklistRecords;
    }

    // This is the test method that calls the getWeekCodes method from the WeekCodesController
    @IsTest
    static void testGetWeekCodes() {
        // Call the Apex method
        List<Picklist__c> weekCodes = WeekCodesController.getWeekCodes();
        
        // Verify that the data is as expected
        System.assertNotEquals(0, weekCodes.size(), 'Week codes should not be empty.');
        System.assertEquals(5, weekCodes.size(), 'There should be 5 week codes.');
        
        for (Picklist__c picklist : weekCodes) {
            System.assert(picklist.Name.startsWith('Week'), 'Each picklist name should start with "Week".');
            System.assert(picklist.Week_Code__c.startsWith('C'), 'Each week code should start with "C".');
        }
    }
}