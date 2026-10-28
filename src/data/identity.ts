export const identity = {
  name: 'Sky Blu DeGrate',
  brand: 'Documentation Princess',
  site: 'https://femalethreat.actor',
  github: 'https://github.com/documentationprincess',
  linkedin: 'https://www.linkedin.com/in/skydegrate/',
};

export const person = {
  '@type': 'Person',
  '@id': `${identity.site}/about#sky`,
  name: identity.name,
  alternateName: identity.brand,
  url: `${identity.site}/about`,
  sameAs: [identity.github, identity.linkedin],
};
