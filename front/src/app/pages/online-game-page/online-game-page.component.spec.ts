import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OnlineGamePageComponent } from './online-game-page.component';

describe('OnlineGamePageComponent', () => {
  let component: OnlineGamePageComponent;
  let fixture: ComponentFixture<OnlineGamePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OnlineGamePageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(OnlineGamePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
