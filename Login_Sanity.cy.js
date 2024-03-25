/// <reference types = "cypress" />

describe('Login Testing', () => {

    const PortalUrl = Cypress.env('PortalUrl')
    const Player = "phpcypresslogin@testaccount.com"
    const Password = "pass.123"
    const suspendPlayer = Cypress.env('suspendPlayer')
    const inactivePlayer = Cypress.env('inactivePlayer')
    const Sign_in = () => {
        cy.visit(PortalUrl)
        cy.get('[data-testid="login-link"]').click() //Sign in Button
    }
    const Term_agree = () => {
        cy.get('[data-testid="term-agree-check"]').should('be.visible').click()
        cy.get('[data-testid="term-agree-submit-btn"]').should('not.be.disabled').click()
    } 

    it('Login Success Checking By Normal', () => {
        // 流程 : 透過 Portal 右上角正常登入按鈕進行登入測試
        // 檢查項目 : Domain / 按鈕
        Sign_in()
        cy.url().should('contain', '/login')
        cy.get(':nth-child(1) > .input__label > .input__inner > input').should('be.visible').type(Player)
        cy.get('[data-testid="input-password"]').type(Password)
        cy.get('[data-testid="login-btn"]').should('not.be.disabled').click()
        Term_agree()
        cy.url().should('contain', '/lobby')
    })

    it('Login Success Checking By SBK', () => {  
        // 流程 : 透過 Portal 左上角漢堡圖示 > SBK 產品進行登入測試
        // 檢查項目 : Domain / 按鈕

        cy.visit('https://aws.sptest.xyz/') //由於 QAT 點擊無效固定前往 STG 測試
        cy.get('[data-testid="hamburger-menu"]').click()
        cy.get('[data-testid="sportsbook-link"] > .icon > img').click()
        cy.location('pathname').should(($pathname) => {
            expect($pathname.endsWith('/sbk/game')).to.be.true
        })
        cy.get('[data-testid="login-link"]').should('be.visible').click()
        cy.get('.input__inner').eq(0).should('be.visible').type(Player);
        cy.get('[data-testid="input-password"]').type(Password)
        cy.get('[data-testid="login-btn"]').should('not.be.disabled').click()
        Term_agree()
        cy.url().should('contain', '/sbk/game')
    })

    it('Login Account Checking', () => {
        // 流程 : 透過 Portal 右上角正常登入按鈕進行登入測試，過程中故意輸入錯誤的"帳號"進行邏輯驗證
        // 檢查項目 : 按鈕 / 錯誤提示 

        Sign_in()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').should('be.visible').type(Player)
        cy.get(':nth-child(1) > .input__label > .input__inner > input').clear()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').blur()
        cy.get('[data-testid="input-warning"]').should('be.visible')
        cy.get('[data-testid="login-btn"]').should('be.disabled')
        cy.get(':nth-child(1) > .input__label > .input__inner > input').type('WrongAccount')
        cy.get('[data-testid="input-password"]').type(Password)
        cy.get('[data-testid="login-btn"]').click()
        cy.get('[data-testid="input-reminder"]').should('be.visible').should('contain', 'Incorrect Username or Password.') // 用户名或密码不正确
    })

    it('Login Password Checking', () => {
        // 流程 : 透過 Portal 右上角正常登入按鈕進行登入測試，過程中故意輸入錯誤的"密碼"進行邏輯驗證
        // 檢查項目 : 按鈕 / 錯誤提示
        
        Sign_in()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').type(Player)
        cy.get('[data-testid="input-password"]').type('12345')
        cy.get('[data-testid="login-btn"]').should('be.disabled')
        cy.get('[data-testid="input-password"]').clear()
        cy.get('[data-testid="input-password"]').type('1234567890123')
        cy.get('[data-testid="login-btn"]').should('be.disabled')
        cy.get('[data-testid="input-password"]').clear()
        cy.get('[data-testid="input-password"]').type('WrongPWD')
        cy.get('[data-testid="login-btn"]').click()
        cy.get('[data-testid="input-reminder"]').should('be.visible').should('contain', 'Incorrect Username or Password.') // 用户名或密码不正确
        
    })

    it('Login Different Account Checking', () => {
        // 流程 : 登入不存在的帳號與 Suspend / Inactive 帳號
        // 檢查項目 : 按鈕 / 錯誤提示

        Sign_in()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').clear()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').type(inactivePlayer)
        cy.get('[data-testid="input-password"]').clear()
        cy.get('[data-testid="input-password"]').type(Password)
        cy.get('[data-testid="login-btn"]').click()
        cy.get('[data-testid="input-reminder"]').should('be.visible').should('contain', 'Incorrect Username or Password.')
        cy.get(':nth-child(1) > .input__label > .input__inner > input').clear()
        cy.get(':nth-child(1) > .input__label > .input__inner > input').type(suspendPlayer)
        cy.get('[data-testid="input-password"]').clear()
        cy.get('[data-testid="input-password"]').type(Password)
        cy.get('[data-testid="login-btn"]').click()
        cy.get('[data-testid="input-reminder"]').should('be.visible').should('contain', 'For security reasons, your account has been frozen. Please contact Customer Service for assistance.') 

    })
})

