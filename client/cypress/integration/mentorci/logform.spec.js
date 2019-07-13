/// <reference types="Cypress" />

function createStudent() {
  cy.get("#add-student").click();
  cy.get("#student-name").type("Uzi Nakamura");
  cy.get("#student-email").type("uzinaks@test.com");
  cy.get("#createStudentForm")
    .find("button")
    .click();
}

function loginMentor() {
  cy.visit("http://localhost:8080");
  cy.get("#login-email").type("testing@test.com");
  cy.get("#login-password").type("testing000");
  cy.get("#loginForm").submit();
}

context("LogForm Page", () => {
  before(() => {
    loginMentor();
    createStudent();
    cy.get('a[href="/profile"]').click();
    cy.get("#logOutBtn").click();
  });

  beforeEach(() => {
    loginMentor();
  });

  it("can create log", () => {
    cy.get('div[testid="Uzi Nakamura"]')
      .find("#logSessionButton")
      .click();
    cy.get("#date").type("2019-07-13");
    cy.get("#mins").type("30");
    cy.get("#sessionTypes").select("intro", { force: true });
    cy.get("#logFormProjects").select("other", { force: true });
    cy.get("#summary").type("We introduced ourselves.");
    cy.get("#createLogForm").submit();
    cy.get(".card-title").should("have.length", 1);
  });

  it("can update log", () => {
    cy.get('a[href="/sessions"]').click();
    cy.get(".card-title")
      .first()
      .click();
    cy.get("#summary")
      .clear()
      .type("just changed the summary.");
    cy.get("#createLogForm").submit();
    cy.get(".card-title").should("have.length", 1);
  });

  it("can delete log", () => {
    cy.get('a[href="/sessions"]').click();
    cy.get(".card-title")
      .first()
      .click();
    cy.get("#deleteLogButton").click();
    cy.get(".card-title").should("have.length", 0);
  });

  after(() => {
    cy.get('a[href="/"]').click();
    cy.get('div[testid="Uzi Nakamura"]')
      .find(".card-title")
      .click();
    cy.get(".fa-pencil-alt").click();
    cy.get("#deleteStudentButton").click();
  });
});
