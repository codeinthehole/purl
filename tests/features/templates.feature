Feature: Use a URL template

    Scenario: No parameters passed
        Given I have the template ''
        When I expand it
        Then I see an empty string
