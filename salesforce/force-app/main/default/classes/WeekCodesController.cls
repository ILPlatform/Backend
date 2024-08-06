public with sharing class WeekCodesController {
    @AuraEnabled(cacheable=true)
    public static List<Picklist__c> getWeekCodes() {
        return [
            SELECT Id, Name, Week_Code__c 
            FROM Picklist__c 
            WHERE RecordTypeId='012P5000001CUEfIAO'
            ORDER BY Week_Code__c];
    }
}