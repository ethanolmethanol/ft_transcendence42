import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateOnlineGamePageComponent } from './create-online-game-page.component';

describe('CreateOnlineGamePageComponent', () => {
  let component: CreateOnlineGamePageComponent;
  let fixture: ComponentFixture<CreateOnlineGamePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateOnlineGamePageComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateOnlineGamePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
