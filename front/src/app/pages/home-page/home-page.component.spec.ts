import { HomePageComponent } from './home-page.component';

describe('HomePageComponent', () => {
  let component: HomePageComponent;

  beforeEach(async () => {
    component = new HomePageComponent();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
