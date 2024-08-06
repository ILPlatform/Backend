public with sharing class WeekCodesPicklistController {
    @AuraEnabled(cacheable=true)
    public static List<String> getWeekCodesPicklist(List<Id> recordIds) {
        List<String> campCodes = new List<String>();

        // Query to get the Week_Code__c field from the selected records
        for (Picklist__c record : [SELECT Week_Code__c FROM Picklist__c WHERE Id IN :recordIds]) {
            campCodes.add(record.Week_Code__c);
        }

        return campCodes;
    }
}