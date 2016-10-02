# Gitem

[![Build Status](https://travis-ci.org/mschwager/gitem.svg?branch=master)](https://travis-ci.org/mschwager/gitem)

`Gitem` is a tool for performing Github organizational reconnaissance.

This could include information for:

* Spearphishing
* Recruitment
* Competitive analysis
* OPSEC self-assessment

# Installing

```
$ pip install gitem
$ gitem -h
```

OR

```
$ git clone https://github.com/mschwager/gitem.git
$ cd gitem
$ pip install --requirement requirements.txt
$ python lib/gitem/__main__.py -h
```

# Using

`Gitem` can be used to collect information at various levels of granularity from Github.

For example, let's grab some information about Facebook:

```
$ gitem organization facebook
Website: https://code.facebook.com/projects/
Username: facebook
Description: We work hard to contribute our work back to the web, mobile, big data, & infrastructure communities. NB: members must have two-factor auth.
Created: 2009-04-02T03:35:22Z
Github URL: https://github.com/facebook
Last Updated: 2016-09-21T15:36:43Z
# of Public Repositories: 173
Location: Menlo Park, California
Organization Name: Facebook
Email Address:
Public Members:
  ...

Public Repositories:
  Repository Name: react
  Watchers: 50773
  Description: A declarative, efficient, and flexible JavaScript library for building user interfaces.
  Created: 2013-05-24T16:15:54Z
  Github URL: https://github.com/facebook/react
  Last Updated: 2016-10-01T15:09:54Z
  Stars: 50773
  Forks: 8855
  Last Pushed: 2016-10-01T14:27:58Z

  Repository Name: react-native
  Watchers: 38364
  Description: A framework for building native apps with React.
  Created: 2015-01-09T18:10:16Z
  Github URL: https://github.com/facebook/react-native
  Last Updated: 2016-10-01T14:37:29Z
  Stars: 38364
  Forks: 8531
  Last Pushed: 2016-10-01T14:15:31Z

  Repository Name: pop
  Watchers: 16481
  Description: An extensible iOS and OS X animation library, useful for physics-based interactions.
  Created: 2014-03-30T22:29:12Z
  Github URL: https://github.com/facebook/pop
  Last Updated: 2016-10-01T14:12:35Z
  Stars: 16481
  Forks: 2630
  Last Pushed: 2016-08-23T17:23:10Z

  ...
```

From here we can drill down into a certain repository:

```
$ gitem repository facebook react
Repository Name: react
Watchers: 50773
Description: A declarative, efficient, and flexible JavaScript library for building user interfaces.
Last Pushed: 2016-10-01T14:27:58Z
Created: 2013-05-24T16:15:54Z
Github URL: https://github.com/facebook/react
Last Updated: 2016-10-01T15:09:54Z
Language: JavaScript
Stars: 50773
Forks: 8855
Homepage: https://facebook.github.io/react/
Contributors:
  Username: zpao
  Contributions: 1755
  Username: spicyj
  Contributions: 1108
  Username: jimfb
  Contributions: 456
  Username: sebmarkbage
  Contributions: 378
  Username: petehunt
  Contributions: 332
  ...
```

And finally, we can analyze specific users:

*Note, this task is easily parallelizable, so we can specify `--processes 4`*

```
$ gitem --processes 4 user <redacted>
Username: <redacted>
Updated: 2016-09-29T02:06:31Z
Name: <redacted>
Created: 2008-04-25T04:38:22Z
Github URL: <redacted>
Company: Facebook
Blog: <redacted>
Location: <redacted>
Email Address: <redacted>
Organizations:
  Organization: facebook
  Organization: reactjs
  Organization: relayjs
Repositories:
  <redacted>
  ...
Emails:
  <redacted>
  ...
```

# Developing

First, install development packages:

```
$ pip install -r requirements-dev.txt
```

## Testing

```
$ nose2
```

## Linting

```
$ flake8
```

## Coverage

```
$ nose2 --with-coverage
```
