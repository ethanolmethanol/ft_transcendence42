import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Oauth42ButtonComponent } from './oauth42-button.component';

describe('Oauth42ButtonComponent', () => {
  let component: Oauth42ButtonComponent;
  let fixture: ComponentFixture<Oauth42ButtonComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Oauth42ButtonComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(Oauth42ButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
