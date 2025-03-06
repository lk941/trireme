import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AutomationSetupComponent } from './automation-setup.component';

describe('AutomationSetupComponent', () => {
  let component: AutomationSetupComponent;
  let fixture: ComponentFixture<AutomationSetupComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AutomationSetupComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AutomationSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
