@isTest
public class WeekCodesPicklistControllerTest {
    @isTest
    public static void testGetWeekCodesPicklist() {
        // Create test data
        List<Picklist__c> picklistRecords = new List<Picklist__c>();
        for (Integer i = 0; i < 5; i++) {
            picklistRecords.add(new Picklist__c(Week_Code__c = 'C' + i));
        }
        insert picklistRecords;

        // Collect the record IDs
        List<Id> recordIds = new List<Id>();
        for (Picklist__c record : picklistRecords) {
            recordIds.add(record.Id);
        }

        // Call the method
        Test.startTest();
        List<String> campCodes = WeekCodesPicklistController.getWeekCodesPicklist(recordIds);
        Test.stopTest();

        // Verify the results
        System.assertEquals(5, campCodes.size(), 'The number of camp codes returned should be 5');
        for (Integer i = 0; i < 5; i++) {
            System.assertEquals('C' + i, campCodes[i], 'The camp code should match the expected value');
        }
    }

    @isTest
    public static void testGetWeekCodesPicklistWithEmptyList() {
        // Create an empty list of IDs
        List<Id> recordIds = new List<Id>();

        // Call the method
        Test.startTest();
        List<String> campCodes = WeekCodesPicklistController.getWeekCodesPicklist(recordIds);
        Test.stopTest();

        // Verify the results
        System.assertEquals(0, campCodes.size(), 'The number of camp codes returned should be 0 for an empty list of IDs');
    }

    @isTest
    public static void testGetWeekCodesPicklistWithNullList() {
        // Call the method with null
        Test.startTest();
        List<String> campCodes = WeekCodesPicklistController.getWeekCodesPicklist(new List<Id>());
        Test.stopTest();

        // Verify the results
        System.assertEquals(0, campCodes.size(), 'The number of camp codes returned should be 0 for a null list of IDs');
    }
}