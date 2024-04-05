Feature: rpgt creates a default configuration

  Scenario: Configuraton is created if missing
    Given we have rpgt installed
    When we run rpgt
    Then return code is "0"
    And we see "created" on stdout
    And we see "loaded" on stdout
    And file "rpgt.conf" is created
